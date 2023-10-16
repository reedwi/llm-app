import Link from "next/link"

import { homeConfig } from "@/config/home"
import { cn } from "@/lib/utils"
import { buttonVariants } from "@/components/ui/button"
import { MainNav } from "@/components/main-nav-pub"
import { auth  } from "@clerk/nextjs";
import supabase from "@/lib/supa"
import { redirect } from "next/navigation"
// import { SiteFooter } from "@/components/site-footer"

interface HomeLayoutProps {
  children: React.ReactNode
}

export default async function HomeLayout({
  children,
}: HomeLayoutProps) {
  const { userId } = auth()
  let label = 'Login'
  let route = '/sign-in'
  if (userId) {
    let data = null;
    let error = null;
  
    const startTime = Date.now(); // save the start time
  
    while (!data || data.length === 0) {
      const response = await supabase
        .from('accounts')
        .select('account_uuid')
        .eq('clerk_id', userId);
  
      data = response.data;
      error = response.error;
  
      if (error) {
        console.error(error);
        break;
      }
  
      // check if more than 3 seconds have passed
      if (Date.now() - startTime > 3000) {
        break;
      }
    }
  
    if (!data || data.length === 0) {
      console.log('no data');
    }
    else {
      try {
        route = `/${data[0].account_uuid}/`;
        label = 'My Account';
        console.log('My account')
      } catch (error) {
        console.log('Error getting account for user');
      }
      redirect(`/${data[0].account_uuid}/install`)
    }
    // const { data } = await supabase
    //                               .from('accounts')
    //                               .select('account_uuid')
    //                               .eq('clerk_id', userId);
    // if (data) {
    //   try {
    //     route = `/${data[0].account_uuid}/`;
    //     label = 'My Account';
    //   } catch (error) {
    //     console.log('Error getting account for user');
    //   }

    // }
  }
  return (
    <div className="flex min-h-screen flex-col">
      <header className="container z-40 bg-background">
        <div className="flex h-20 items-center justify-between py-6">
          <MainNav items={homeConfig.mainNav} />
          <nav>
            <Link
              href={route}
              className={cn(
                buttonVariants({ variant: "secondary", size: "sm" }),
                "px-4"
              )}
            >
              {label}
            </Link>
          </nav>
        </div>
      </header>
      <main className="flex-1">{children}</main>
      {/* <SiteFooter /> */}
    </div>
  )
}