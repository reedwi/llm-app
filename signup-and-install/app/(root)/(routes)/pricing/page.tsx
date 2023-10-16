
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { cn } from "@/lib/utils"
import { buttonVariants } from "@/components/ui/button"
import { auth  } from "@clerk/nextjs";
import { Icons } from "@/components/ui/icons"

export const metadata = {
  title: "Pricing"
}

function Container({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "flex items-center justify-center [&>div]:w-full",
        className
      )}
      {...props}
    />
  )
}

export default function PricingPage() { 
  const { userId } = auth();
  const standardPaymentUrl = process.env.STANDARD_PAYMENT_URL ? process.env.STANDARD_PAYMENT_URL: "";
  const premiumPaymentUrl = process.env.STANDARD_PAYMENT_URL ? process.env.STANDARD_PAYMENT_URL: "";
  const standardUrl = userId ? standardPaymentUrl: '/sign-up';
  const premiumUrl = userId ? premiumPaymentUrl: '/sign-up';
  const entUrl = "/pricing";

  const buttonLabel = userId ? "Get Started": "Sign Up";

  return (
    <>
      <section className="container flex flex-col  gap-6 py-8 md:max-w-[64rem] md:py-12 lg:py-24">
      <div className="mx-auto flex w-full flex-col gap-4 md:max-w-[58rem]">
        <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl">
          Simple, transparent pricing
        </h2>
        <p className="max-w-[85%] leading-normal text-muted-foreground sm:text-lg sm:leading-7">
          Unlock all features as described below.
        </p>
      </div>
      <div className="hidden items-start justify-center gap-6 rounded-lg p-8 md:grid lg:grid-cols-2 xl:grid-cols-3">
        <div className="grid gap-4 rounded-lg border p-4"> 
          <h3 className="text-xl font-bold sm:text-2xl">
            What&apos;s included in the Standard plan
          </h3>
          <ul className="col-span-2 grid items-start gap-2">
            
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Unlimited Users
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Unlimited Chatbots
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Support
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Usage Statistics
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> 1,000 prompts
            </li>
          </ul>
        <div className="grid gap-4 text-center">
          <div>
            <h4 className="text-7xl font-bold">$99</h4>
            <p className="text-sm font-medium text-muted-foreground">
              Billed Monthly
            </p>
          </div>
          <Link href={standardUrl} className={cn(buttonVariants({ size: "lg" }))}>
            {buttonLabel}
          </Link>
        </div>
        </div>
        <div className="grid gap-4 rounded-lg border p-4"> 
          <h3 className="text-xl font-bold sm:text-2xl">
            What&apos;s included in the Premium plan
          </h3>
          <ul className="col-span-2 grid items-start gap-2">
            
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Unlimited Users
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Unlimited Chatbots
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Premium Support
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Usage Statistics
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> 10,000 prompts
            </li>
            
          </ul>
        <div className="grid gap-4 text-center">
          <div>
            <h4 className="text-7xl font-bold">$299</h4>
            <p className="text-sm font-medium text-muted-foreground">
              Billed Monthly
            </p>
          </div>
          <Link href={premiumUrl} className={cn(buttonVariants({ size: "lg" }))}>
            {buttonLabel}
          </Link>
        </div>
        </div>
        <div className="grid gap-4 rounded-lg border p-4"> 
          <h3 className="text-xl font-bold sm:text-2xl">
            What&apos;s included in the Enterprise plan
          </h3>
          <ul className="col-span-2 grid items-start gap-2">
            
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Unlimited Users
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Unlimited Chatbots
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Premium Support
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Usage Statistics
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Prompts as Needed
            </li>
            <li className="flex items-center">
              <Icons.check className="mr-2 h-4 w-4" /> Custom built models
            </li>
          </ul>
        <div className="grid gap-4 text-center">
          <div>
            <h4 className="text-3xl font-bold">Custom Pricing</h4>
            <p className="text-sm font-medium text-muted-foreground">
              Billed Monthly
            </p>
          </div>
          <Link href={entUrl} className={cn(buttonVariants({ size: "lg" }))}>
            {buttonLabel}
          </Link>
        </div>
        </div>
      </div>

      <div className="mx-auto flex w-full max-w-[58rem] flex-col gap-4">
        <p className="max-w-[100%] leading-normal text-muted-foreground sm:leading-7">
          YakBots is currently in a beta phase.{" "}
          <strong>If you encounter any issues please reachout to support@theobogroup.com.</strong>
        </p>
      </div>
    </section>
    </>
  )
}