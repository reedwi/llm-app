import { NextResponse } from "next/server";

import supabase from "@/lib/supa";

export async function POST(
  req: Request,
) {
  try {
    const body = await req.json();
    const startDate: Date = new Date();
    startDate.setHours(0, 0, 0, 0); // set the time to midnight
    
    const endDate: Date = new Date(startDate.getTime()); // copy the start date
    endDate.setMonth(startDate.getMonth() + 1);

    const account = await supabase.from('accounts').insert([
      { 
        install_email: body.data.email_addresses[0].email_address,
        clerk_id: body.data.id,
        account_status: 'TRIAL',
        subscription_start_date: startDate.toISOString(),
        subscription_end_date: endDate.toISOString(),
      }
    ]);

    return NextResponse.json(account);
  } catch (error) {
    console.log('[ACCOUNTS_POST]', error);
    return new NextResponse("Internal error", { status: 500 });
  }
}