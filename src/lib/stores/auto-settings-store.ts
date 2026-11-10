import { Store } from "@tanstack/store";

type AutoSettingsStore = {
    /**
     * Whether auto forward is enabled
     */
    enabled: boolean;
    /**
     * Time in seconds to wait before auto forwarding
     */
    time: number;
};

const ENABLED_KEY = "auto_forward_enabled";

export namespace AutoSettings {
    export const store = new Store<AutoSettingsStore>({
        // Stored as "true"/"false"; Boolean("false") would be true (R-02).
        enabled: localStorage.getItem(ENABLED_KEY) === "true",
        time: Number(localStorage.getItem("auto_forward_second") ?? 1),
    });

    /**
     * Toggle the auto forward state
     */
    export function toggleEnabled() {
        setEnabled(!store.state.enabled);
    }

    /**
     * Set the auto forward state. Persisted like the settings switch, so the
     * quick-tools toggle and the settings screen agree after a reload.
     */
    export function setEnabled(value: boolean) {
        localStorage.setItem(ENABLED_KEY, value.toString());
        store.setState((state) => ({ ...state, enabled: value }));
    }

    /**
     * Set the time to wait before auto forwarding
     */
    export function setTime(value: number) {
        localStorage.setItem("auto_forward_second", value.toString());
        store.setState((state) => ({ ...state, time: value }));
    }
}
