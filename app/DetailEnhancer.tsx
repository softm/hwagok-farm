"use client";
import { useEffect } from "react";
import { usePathname } from "next/navigation";
export default function DetailEnhancer() {
  const pathname = usePathname();
  useEffect(() => {
    const root = document.querySelector(".detail-page,.record-page,[data-record-page]");
    if (!root) { document.documentElement.removeAttribute("data-record-detail"); return; }
    document.documentElement.setAttribute("data-record-detail", "compact-v1");
    const ready = () => window.dispatchEvent(new Event("archive:detail-ready"));
    const existing = document.getElementById("record-detail-script");
    if (existing) { ready(); return; }
    const script = document.createElement("script");
    script.id = "record-detail-script";
    script.src = `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/archive-detail.js?v=20260930-compact-v1`;
    script.defer = true;
    script.addEventListener("load", ready, { once: true });
    document.body.appendChild(script);
  }, [pathname]);
  return null;
}
