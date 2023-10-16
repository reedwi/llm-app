
import Link from "next/link"
import { cn } from "@/lib/utils"
import { Button, buttonVariants } from "@/components/ui/button"
import { Icons } from "@/components/ui/icons"
import { Url } from "url"

interface EnterprisePricingProps {
  href: any
}

const EnterprisePricing = async ({ href }: EnterprisePricingProps) => {
  return (
    <div className="grid gap-4 rounded-lg border p-4 flex-col h-full"> 
      <h3 className="text-xl font-bold sm:text-2xl">
        What&apos;s included in the Enterprise plan
      </h3>
      <ul className="col-span-2 grid items-start gap-2">
        
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Custom Users
        </li>
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Unlimited Questions & Answers
        </li>
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Unlimited Document Uploads
        </li>
        <li className="flex items-center">
          <Icons.check className="mr-2 h-4 w-4" /> Custom File Size Compatability
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
          <Icons.check className="mr-2 h-4 w-4" /> +10GB Storage
        </li>
      </ul>
    <div className="grid gap-4 text-center">
      <div>
        <h4 className="text-3xl font-bold">Custom Pricing</h4>
        <p className="text-sm font-medium text-muted-foreground">
          Billed Monthly
        </p>
      </div>
      <Button >
      <a target="_blank" href={href} rel="noopener noreferrer" >Contact Us</a>
      </Button>
      
    </div>
    </div>
  );
}

export default EnterprisePricing;