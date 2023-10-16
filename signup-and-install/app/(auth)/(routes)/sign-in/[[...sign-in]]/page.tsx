import { SignIn, auth } from "@clerk/nextjs";
import supabase from "@/lib/supa";

export default async function Page() {
  return <SignIn afterSignInUrl={'/'}/>;
};