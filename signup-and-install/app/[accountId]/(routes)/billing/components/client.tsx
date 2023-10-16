"use client";

import { DataTable } from "@/components/ui/data-table";
import { Heading } from "@/components/ui/heading";
import { Separator } from "@/components/ui/separator";

import { columns, PaymentsColumn } from "./columns";

interface PaymentsClientProps {
  data: PaymentsColumn[];
}

export const PaymentsClient: React.FC<PaymentsClientProps> = ({
  data
}) => {
  return (
    <>
      <Heading title={`Payments (${data.length})`} description="View payment history" />
      <Separator />
      <DataTable searchKey="product" columns={columns} data={data} />
    </>
  );
};