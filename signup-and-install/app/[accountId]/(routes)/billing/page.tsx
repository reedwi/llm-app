
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { cn, formatter } from "@/lib/utils"
import { Button, buttonVariants } from "@/components/ui/button"
import { auth  } from "@clerk/nextjs";
import { Icons } from "@/components/ui/icons"
import { format } from "date-fns"
import supabase from "@/lib/supa";
import { redirect } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import StandardPricing from "@/components/standard-pricing";
import PremiumPricing from "@/components/premium-pricing";
import EnterprisePricing from "@/components/enterprise-pricing";
import { PaymentsColumn } from "./components/columns";
import { PaymentsClient } from "./components/client";

export const metadata = {
  title: "Billing"
}


const BillingPage = async ({
  params
}: {
  params: { accountId: string }
}) => { 
  const { userId } = auth();
  const { data, error } = await supabase
    .from('accounts')
    .select('id, install_email, account_status, subscription_start_date, subscription_end_date, clerk_id')
    .eq('account_uuid', params.accountId)
  ;
  
  if (!data) {
    redirect('/');
  }

  if (data[0].clerk_id !== userId) {
    redirect('/')
  }

  let paymentsComponent = null
  const payments = await supabase
    .from('payments')
    .select('name, payment_date, next_payment_date, amount')
    .eq('account_uuid', params.accountId)
    .order('payment_date', { ascending: false });
  
  if (payments.data && payments.data.length !== 0) {
    const formattedPayments: PaymentsColumn[] = payments.data.map((payment) => ({
      product: payment.name,
      amount: formatter.format(payment.amount),
      payment_date: format(new Date(payment.payment_date), "MM-dd-yyyy"),
      next_date: format(new Date(payment.next_payment_date), "MM-dd-yyyy")
    }));
    paymentsComponent =
      <div className="flex-col">
      <div className="flex-1 space-y-4 p-8 pt-6">
        <PaymentsClient data={formattedPayments}/>
      </div>
    </div>
  }
  


  const email = data[0].install_email
  const status = data[0].account_status
  const startDate = data[0].subscription_start_date
  const endDate = data[0].subscription_end_date
  const accountId = data[0].id;
  const nonCustomer = [null, '',]
  let component = null
  let upgradeComponent = null


  // Check if user is currently subscribed and display a upgrade/cancel screen
  const standardPaymentUrl = process.env.STANDARD_PAYMENT_URL ? process.env.STANDARD_PAYMENT_URL+ `&email=${email}&yakbots_id=${params.accountId}`: "";
  const premiumPaymentUrl = process.env.STANDARD_PAYMENT_URL ? process.env.STANDARD_PAYMENT_URL+ `&email=${email}&yakbots_id=${params.accountId}`: "";
  const standardUrl = userId ? standardPaymentUrl: '/sign-up';
  const premiumUrl = userId ? premiumPaymentUrl: '/sign-up';
  const entUrl = process.env.ENT_URL ? process.env.ENT_URL+ `?email=${email}`: "";
  const buttonLabel = userId ? "Upgrade": "Sign Up";
  const standardDisabled = status === 'STANDARD' ? true : false;
  const cancelUrl = process.env.CANCEL_FORM_URL ? process.env.CANCEL_FORM_URL+ `?email=${email}`: "";

  // Add in link to Monday free trial link and Slack trial link for people that are not current customers
  const pricingComponent = <>
  <section className="container flex flex-col  gap-6 py-6 md:max-w-[64rem] md:py-6 lg:py-6">
  <div className="mx-auto flex w-full flex-col gap-4 md:max-w-[58rem]">
    <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl">
      Simple, transparent pricing
    </h2>
    <p className="max-w-[85%] leading-normal text-muted-foreground sm:text-lg sm:leading-7">
      Unlock all features as described below.
    </p>
  </div>
  <div className="hidden items-start justify-center gap-6 rounded-lg p-8 md:grid lg:grid-cols-2 xl:grid-cols-3">
    <StandardPricing href={standardUrl} />
    <PremiumPricing href={premiumUrl} />
    <EnterprisePricing href={entUrl} />
  </div>

  <div className="mx-auto flex w-full max-w-[58rem] flex-col gap-4">
    <p className="max-w-[100%] leading-normal text-muted-foreground sm:leading-7">
      YakBots is currently in a beta phase.{" "}
      <strong>If you encounter any issues please reachout to support@theobogroup.com.</strong>
    </p>
  </div>
</section>
</>
  if (nonCustomer.includes(status)) {
    upgradeComponent = pricingComponent;
  }
  // else if (status === 'STANDARD') {
  //   upgradeComponent = 
  // }
  if (nonCustomer.includes(status)) {
    component = pricingComponent
  }
  else {
    const { data, error } = await supabase
      .from('current_usage')
      .select('query_count')
      .eq('account_id', accountId)
    ;
    let usage: Number;
    if (!data || data.length === 0) {
      usage = 0;
    }
    else {
      usage = data[0].query_count;
    }

    component =
    <>
    <section className="container flex flex-col  gap-6 py-2 md:max-w-[64rem] md:py-6 lg:py-10">
      <div className="mx-auto flex w-full flex-col gap-4 md:max-w-[58rem]">
      <div className="flex justify-between items-center w-full">
      <h2 className="font-heading text-2xl leading-[1.1] sm:text-2xl md:text-4xl">
        Account and Billing Information
      </h2>
      <Button >
          <a target="_blank" href={cancelUrl} rel="noopener noreferrer">Cancel Account</a>
        </Button>
          </div>
      <p className="max-w-[85%] leading-normal text-muted-foreground sm:text-lg sm:leading-7">
        View usage, upgrade and cancel your account
      </p>
    </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Current Tier
          </CardTitle>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            className="h-4 w-4 text-muted-foreground"
          >
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
          </svg>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{status}</div>
          <p className="text-xs text-muted-foreground">
          </p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Prompts Used this Month
          </CardTitle>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            className="h-4 w-4 text-muted-foreground"
          >
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
          </svg>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{String(usage)}/1000</div>
          <p className="text-xs text-muted-foreground">
          </p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Cycle Start Date 
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{startDate?.slice(0,10)}</div>
          <p className="text-xs text-muted-foreground">
          </p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Cycle End Date
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{endDate?.slice(0,10)}</div>
          <p className="text-xs text-muted-foreground">
          </p>
        </CardContent>
      </Card>
      {/* <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
          </CardTitle>
        </CardHeader>
        <CardContent className="flex justify-center items-center">
          <Link href={cancelUrl} className={cn(buttonVariants({ size: "lg" }))}>
            Cancel Account
          </Link>
        </CardContent>
      </Card> */}
      
      </div>
      {paymentsComponent}
    </section>
    {pricingComponent}
    </>
  }
  // Build a component that
  // Button to upgrade if on standard, show current usage for month, button to cancel
  return (
    component
  )
}
export default BillingPage;