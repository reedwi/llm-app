import { NextResponse } from "next/server";

import supabase from "@/lib/supa";

export async function POST(
  req: Request,
) {
  try {
    const body = await req.json();

    const payment = await supabase.from('payments').insert([
      { 
        name: body?.name,
        amount: body?.amount,
        start_date: body?.start_date,
        end_date: body?.end_date
      }
    ]);

    return NextResponse.json(payment);
  } catch (error) {
    console.log('[PAYMENTS_POST]', error);
    return new NextResponse("Internal error", { status: 500 });
  }
}