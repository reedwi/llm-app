import { redirect } from 'next/navigation';
import { auth  } from "@clerk/nextjs";
import supabase from "@/lib/supa"
import Navbar from '@/components/navbar';


export default async function SetupLayout({
  children,
  params
}: {
  children: React.ReactNode,
  params: { accountId: string }
}) {
  const { userId } = auth();
  if (!userId) {
    redirect('/sign-in');
  }
  
  const { data, error } = await supabase
    .from('accounts')
    .select('account_uuid, clerk_id')
    .eq('account_uuid', params.accountId);
  
  if (!data) {
    redirect('/');
  }

  if (data[0].clerk_id !== userId) {
    redirect('/')
  }

  return (
    <>
      <Navbar />
      {children}
    </>
  );
};