"use client"

import { ColumnDef } from "@tanstack/react-table"

export type DocsColumn = {
  doc: string;
  description: string;
  link: string;
}

export const columns: ColumnDef<DocsColumn>[] = [
  {
    accessorKey: "doc",
    header: "Doc Title",
  },
  {
    accessorKey: "description",
    header: "Description",
  },
  {
    accessorKey: "link",
    header: "Link",
    cell: ({ row }) => (
      <a className="text-orange" target="_blank" href={row.original.link} rel="noopener noreferrer">View Documentation</a>
    )
  },
];