import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "화곡농장 프로젝트",
  description: "화곡농장 프로젝트의 채팅별 작업계획과 현장자료를 한곳에 모은 중앙 사이트입니다.",
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
