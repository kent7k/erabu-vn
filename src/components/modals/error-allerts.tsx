import { Button } from "@/components/ui/button";
import { useNetworkDetector } from "@/lib/hooks/network-hooks";
import { WifiOffIcon, XIcon } from "lucide-react";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

/**
 * A small banner, not a full-screen block (R-01): the script is in the bundle and
 * images/audio already loaded (or cached by the service worker) keep working offline,
 * so the game should stay playable. The banner can be dismissed and comes back the
 * next time the connection drops.
 */
export function OfflineAllert() {
    const { t } = useTranslation(["ui"]);
    const { isOnline } = useNetworkDetector();
    const [dismissed, setDismissed] = useState(false);

    useEffect(() => {
        if (isOnline) setDismissed(false);
    }, [isOnline]);

    if (isOnline || dismissed) return null;

    return (
        <div
            role="status"
            data-slot="card"
            className="fixed top-3 left-1/2 z-[120] flex max-w-[calc(100%-2rem)] -translate-x-1/2 items-center gap-3 rounded-xl border border-destructive/30 bg-background/90 py-2 pr-2 pl-4 text-sm shadow-lg backdrop-blur-md animate-in fade-in-0"
        >
            <WifiOffIcon className="size-4 shrink-0 text-destructive" />
            <div className="min-w-0">
                <div className="font-medium">{t("offline_title")}</div>
                <div className="text-xs text-muted-foreground">{t("offline_description")}</div>
            </div>
            <Button
                variant="ghost"
                size="icon"
                onClick={() => setDismissed(true)}
                aria-label={t("offline_dismiss")}
            >
                <XIcon className="size-4" />
            </Button>
        </div>
    );
}
