import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "softm 프로젝트 허브",
  description: "화곡농장, 웅도, 서해박속낙지와 가족여행의 채팅별 배포 페이지를 한곳에 모은 중앙 사이트입니다.",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
