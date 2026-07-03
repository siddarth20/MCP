import asyncio
from contextlib import AsyncExitStack

from mcp import ClientSession
# Uses the correct, non-deprecated transport client string
from mcp.client.streamable_http import streamable_http_client

from config.settings import PLAYWRIGHT_MCP_URL


class MCPClient:

    def __init__(self):
        self.session = None
        self._exit_stack = None
        # Ensures that heartbeat pings and structural disconnections never collide
        self._lock = asyncio.Lock()
        self._heartbeat_task = None

    async def connect(self):
        """
        Connects to an already-running Playwright MCP server.
        Maintains an internal session lock to guarantee safe startup/shutdown states.
        """
        async with self._lock:
            if self.session:
                return self.session  # Return existing open session

            self._exit_stack = AsyncExitStack()
            
            try:
                # 1. Establish the modern streamable HTTP transport streams
                (read_stream, write_stream, _) = await self._exit_stack.enter_async_context(
                    streamable_http_client(PLAYWRIGHT_MCP_URL)
                )

                # 2. Bind the transport layer to the MCP client session
                self.session = await self._exit_stack.enter_async_context(
                    ClientSession(read_stream, write_stream)
                )

                # 3. Synchronize protocols via initialization handshake
                await self.session.initialize()
                print(f"\n[MCP] Connected to Playwright MCP at {PLAYWRIGHT_MCP_URL}")

                # 4. Pull available tool definitions to verify connectivity
                tools = await self.session.list_tools()
                print(f"[MCP] Loaded {len(tools.tools)} tools")

                # 5. Spin up a background keep-alive heartbeat loop
                self._heartbeat_task = asyncio.create_task(self._keep_alive_loop())
                return self.session

            except Exception as e:
                print(f"[MCP] Connection initialization failed: {e}")
                await self._force_cleanup()
                raise

    async def _keep_alive_loop(self):
        """Periodically pings the server every 30 seconds to prevent timeouts."""
        try:
            while True:
                await asyncio.sleep(30)
                
                # Check session health within a thread-safe context lock
                async with self._lock:
                    if not self.session:
                        break
                    # Querying tools is the safest, low-overhead keep-alive ping
                    await self.session.list_tools()
                    
        except asyncio.CancelledError:
            pass  # Expected cleanup behavior when disconnecting
        except Exception as e:
            print(f"\n[Warning] Heartbeat noticed connection was dropped: {e}")
            # Offload cleanup to a separate task string to avoid AnyIO cancel scope mixing
            asyncio.create_task(self._handle_unexpected_disconnect())

    async def _handle_unexpected_disconnect(self):
        """Safely clean up dead memory states without conflicting with active tasks."""
        async with self._lock:
            if self.session:
                print("[MCP] Cleaning up stale session context...")
                await self._force_cleanup()

    async def _force_cleanup(self):
        """Internal helper that explicitly clears background tasks and stack context."""
        if self._heartbeat_task and not self._heartbeat_task.done():
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except Exception:
                pass
            self._heartbeat_task = None
            
        if self._exit_stack:
            try:
                # Catch AnyIO cross-task cancellation errors during unexpected stack pops
                await self._exit_stack.aclose()
            except RuntimeError as re:
                if "cancel scope" in str(re):
                    pass  # Suppress AnyIO race conditions
                else:
                    raise re
            except Exception:
                pass
                
        self._exit_stack = None
        self.session = None

    async def disconnect(self):
        """Explicitly and gracefully closes the session and clears structures."""
        async with self._lock:
            if not self.session:
                print("[MCP] Client is already disconnected.")
                return
                
            print("\n[MCP] Disconnecting from Playwright MCP...")
            await self._force_cleanup()
            print("[MCP] Disconnected successfully.")

    async def call_tool(self, name: str, arguments: dict):
        """
        Executes an MCP tool call. Intercepts abrupt mid-execution crashes 
        and flags the session state for clean isolation.
        """
        if not self.session:
            raise RuntimeError("MCP Client is not connected. Call connect() first.")

        try:
            # Execute without holding the lock so heartbeat checks don't block tool execution
            return await self.session.call_tool(name, arguments=arguments)
        except Exception as e:
            err_str = str(e).lower()
            if "terminated" in err_str or "404" in err_str or "closed" in err_str:
                print(f"\n[MCP] Connection lost or closed during tool '{name}' execution.")
                asyncio.create_task(self._handle_unexpected_disconnect())
            raise


# --- Direct Test Entrypoint ---
# Uncomment to test file resilience directly against your server:
#
# async def main():
#     client = MCPClient()
#     await client.connect()
#     try:
#         while True:
#             await asyncio.sleep(1)
#     except KeyboardInterrupt:
#         await client.disconnect()
#
# if __name__ == "__main__":
#     asyncio.run(main())