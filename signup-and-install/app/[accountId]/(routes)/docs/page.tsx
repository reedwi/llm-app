

import supabase from "@/lib/supa";

import { DocsColumn } from "./components/columns"
import { DocsClient } from "./components/client";
import { redirect } from "next/navigation";

const DocsPage = async ({
  params
}: {
  params: { accountId: string }
}) => {
  const { data, error } = await supabase
    .from('docs')
    .select('id, title, description, link')
    .order('id', {ascending: false})
  ;
  
  if (!data) {
    redirect('/');
  }

  const formattedDocs: DocsColumn[] = data.map((item) => ({
    doc: item.title,
    description: item.description,
    link: item.link,
  }));

  return (
    <div className="flex-col">
      <div className="flex-1 space-y-4 p-8 pt-6">
        <DocsClient data={formattedDocs} />
      </div>
    </div>
  );
};

export default DocsPage;