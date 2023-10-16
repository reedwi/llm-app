
import { SignUp } from "@clerk/nextjs";
import { useSearchParams } from "next/navigation";

export default function Page() {
  // const searchParams = useSearchParams();
  // const product = searchParams.get('product');
  // console.log(product);
  // const url = product === 'standard' ? process.env.STANDARD_PAYMENT_URL :
  //             product === 'premium' ? process.env.PREMIUM_PAYMENT_URL : '/';

  return <SignUp redirectUrl="/"/>;
};