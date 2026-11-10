import { Store } from "@tanstack/store";

/**
 * The only URL search params the game owns (menus and dialogs). Anything else in
 * the URL (utm_source, fbclid, ...) must stay out of the store: every non-undefined
 * value counts as "a menu is open", which pauses the canvas and blocks goNext (R-27).
 */
export const MENU_PARAMS = ["settings", "settings_tab", "history", "saves"] as const;

export namespace SearchParams {
    export const store = new Store<Record<string, unknown>>({});

    /**
     * Set the value of a URL search param in the store.
     * Pass `undefined` to clear the param.
     */
    export function set(field: string, value: unknown) {
        store.setState((state) => ({ ...state, [field]: value }));
    }

    /**
     * Set multiple search params at once. This is more efficient than calling `set()` multiple times since it only triggers one state update.
     */
    export function setMany(values: Record<string, unknown>) {
        const known = Object.fromEntries(
            Object.entries(values).filter(([key]) =>
                (MENU_PARAMS as readonly string[]).includes(key),
            ),
        );
        store.setState((state) => ({ ...state, ...known }));
    }
}
