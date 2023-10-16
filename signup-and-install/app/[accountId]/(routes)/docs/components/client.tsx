"use client";

import { DataTable } from "@/components/ui/data-table";
import { Heading } from "@/components/ui/heading";
import { Separator } from "@/components/ui/separator";

import { columns, DocsColumn } from "./columns";

interface DocsClientProps {
  data: DocsColumn[];
}

export const DocsClient: React.FC<DocsClientProps> = ({
  data
}) => {
  return (
    <>
      <Heading title={`Docs (${data.length})`} description="View documentation" />
      <Separator />
      <DataTable searchKey="doc" columns={columns} data={data} />
    </>
  );
};