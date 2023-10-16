
import Link from "next/link"
import { cn } from "@/lib/utils"
import { Button, buttonVariants } from "@/components/ui/button"
import { Icons } from "@/components/ui/icons"
import { Url } from "url"

interface StandardPricingProps {
  href: any
}

const StandardPricing = async ({ href }: StandardPricingProps) => {
  return (
    <div className="grid gap-4 rounded-lg border p-4 flex-col h-full"> 
      <h3 className="text-xl font-bold sm:text-2xl">
        What&apos;s included in the Free plan
      </h3>
      <ul className="col-span-2 grid items-start gap-2">
      <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> 1 user
        </li>
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Up to 50 prompts
        </li>
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Up to 20 Document Uploads
        </li>
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Up to 200MB Per File
        </li>
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Email Support
        </li>
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Usage Statistics
        </li>
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Slack Integration
        </li>
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Storage up to 500 mb
        </li>
      </ul>
      <div className="grid gap-4 text-center">
        <div>
          <h4 className="text-7xl font-bold">$0</h4>
        </div>
      </div>
    </div>
  );
}

export default StandardPricing;