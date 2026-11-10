import { routeTree } from "@/routeTree.gen";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createMemoryHistory, createRouter, RouterProvider } from "@tanstack/react-router";

// Every query reads the engine's local state (nothing goes over the network), so it
// must keep running offline. With the default networkMode "online", TanStack Query
// pauses refetches when the browser goes offline and the dialogue stops updating:
// clicks and Enter advance the engine but the screen never changes (R-01).
const queryClient = new QueryClient({
    defaultOptions: {
        queries: { networkMode: "always" },
        mutations: { networkMode: "always" },
    },
});
const router = createRouter({
    routeTree,
    // itch.io は iframe のサブパスで動く。URL を書き換えると相対パスが壊れるので、経路はメモリに持つ（hash も駄目だった）
    history:
        import.meta.env.MODE === "itch"
            ? createMemoryHistory({ initialEntries: ["/"] })
            : undefined,
    defaultPreload: "intent",
    scrollRestoration: true,
    context: { queryClient },
});

declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router;
    }
}

export default function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <RouterProvider router={router} />
        </QueryClientProvider>
    );
}
