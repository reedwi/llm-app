"use client"

import { ColumnDef } from "@tanstack/react-table"

export type PaymentsColumn = {
  product: string;
  amount: string;
  payment_date: string;
  next_date: string;
}

export const columns: ColumnDef<PaymentsColumn>[] = [
  {
    accessorKey: "product",
    header: "Product",
  },
  {
    accessorKey: "amount",
    header: "Amount",
  },
  {
    accessorKey: "payment_date",
    header: "Payment Date"
  },
  {
    accessorKey: "next_date",
    header: "Next Payment Date"
  },
];