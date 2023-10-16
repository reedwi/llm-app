"use client";

import { useParams, usePathname } from "next/navigation";
import { useSelectedLayoutSegment } from "next/navigation"
import Link from "next/link";
import Image from "next/image";
import ybLogo from "@/public/yb-logo-v2.svg"
import { siteConfig } from "@/config/site"

import { cn } from "@/lib/utils";

export function MainNav({
  className,
  ...props
}: React.HTMLAttributes<HTMLElement>) {
  const segment = useSelectedLayoutSegment()
  const pathname = usePathname();
  const params = useParams();

  const routes = [
    // {
    //   href: `/${params.accountId}`,
    //   title: 'Home',
    //   disabled: pathname === `/${params.accountId}`
    // },
    {
      href: `/${params.accountId}/billing`,
      title: 'Billing',
      disabled: pathname === `/${params.accountId}/billing`
    },
    // {
    //   href: `/${params.accountId}/profile`,
    //   title: 'Profile',
    //   disabled: pathname === `/${params.accountId}/profile`
    // },
    {
      href: `/${params.accountId}/install`,
      title: 'Install Instructions',
      disabled: pathname === `/${params.accountId}/install`
    },
    {
      href: `/${params.accountId}/docs`,
      title: 'Docs',
      disabled: pathname === `/${params.accountId}/docs`
    },
  ];

  return (

    <div className="flex gap-6 md:gap-10">
      <Link href="/" className="hidden items-center space-x-2 md:flex">
        <div className="rounded-full overflow-hidden">
          <Image
            priority
            src={ybLogo}
            alt="YakBot"
            height={12}
            width={12}
            className="h-12 w-12 fill-current"
            style={{ border: "none" }}
          />
        </div>
        <span className="hidden font-bold sm:inline-block">
          {siteConfig.name}
        </span>
      </Link>
      {routes?.length ? (
        <nav className="hidden gap-6 md:flex">
          {routes?.map((route) => (
            <Link
              key={route.href}
              href={route.disabled ? "#" : route.href}
              className={cn(
                "flex items-center text-lg font-medium transition-colors hover:text-foreground/80 sm:text-sm",
                route.href.startsWith(`/${segment}`)
                  ? "text-foreground"
                  : "text-foreground/60",
                route.disabled && "cursor-not-allowed opacity-80"
              )}
            >
              {route.title}
            </Link>
          ))}
        </nav>
      ) : null}
  </div>
  )
};