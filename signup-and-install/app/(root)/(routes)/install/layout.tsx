import { redirect } from 'next/navigation';
import { auth  } from "@clerk/nextjs";
import supabase from "@/lib/supa"
import Navbar from '@/components/navbar';

export default async function InstallLayout({
  children
}: {
  children: React.ReactNode,
}) {
  const { userId } = auth();
  if (!userId) {
    redirect('/sign-in');
  }

  const { data, error } = await supabase
    .from('accounts')
    .select('account_uuid')
    .eq('clerk_id', userId);

  if (!data) {
    redirect('/sign-in');
  }

  try {
    redirect(`/${data[0].account_uuid}/install`);
  } catch (error) {
    redirect('/');
  }

  return (
    <>
      <Navbar />
      {children}
    </>
  );
};