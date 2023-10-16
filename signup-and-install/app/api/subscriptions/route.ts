import { NextResponse } from "next/server";

import supabase from "@/lib/supa";

export async function POST(
  req: Request,
) {
  try {
    const body = await req.json();

    const subscription = await supabase.from('subscriptions').insert([
      { 
        name: body?.name,
        amount: body?.amount,
        start_date: body?.start_date,
        end_date: body?.end_date
      }
    ]);

    return NextResponse.json(subscription);
  } catch (error) {
    console.log('[SUBSCRIPTIONS_POST]', error);
    return new NextResponse("Internal error", { status: 500 });
  }
}