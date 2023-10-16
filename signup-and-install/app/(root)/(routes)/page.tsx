'use client'

import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { cn } from "@/lib/utils"
import { buttonVariants } from "@/components/ui/button"
import Image from "next/image"
import monday from "@/public/monday.png"
import MondayIcon from "@/public/monday-icon.svg"
import SlackIcon from "@/public/slack-new-logo.svg"
import FileFolder from "@/public/file-folder.svg"
import Checkmark from "@/public/checkmark.svg"
import UserAdoption from "@/public/user-adoption.svg"
import Trend from "@/public/trend.svg"

export default function HomePage() {

  return (
    <>
      <section className="space-y-6 pb-8 pt-6 md:pb-12 md:pt-10 lg:py-32">
        <div className="container flex max-w-[64rem] flex-col items-center gap-4 text-center">
          <h1 className="font-heading text-3xl sm:text-5xl md:text-6xl lg:text-7xl">
                Chat your own documents using tools you already know.
          </h1>
          <p className="max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
                Use monday.com to build and manage your internal chatbots and Slack to deploy them to your end-users.
          </p>
          <div className="space-x-4">
            <Link href="/pricing" className={cn(buttonVariants({ size: "lg" }))}>
              Get Started
            </Link>
          </div>
        </div>
      </section>
      <section
        id="features"
        className="container space-y-6 bg-slate-50 py-8 dark:bg-transparent md:py-12 lg:py-24"
      >
        <div className="mx-auto flex max-w-[58rem] flex-col items-center space-y-4 text-center">
          <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl">
            Features
          </h2>
          <p className="max-w-[85%] leading-normal text-muted-foreground sm:text-lg sm:leading-7">
            Build, manage, and maintain custom chatbots based on your data using monday.com and Slack.
          </p>
        </div>
        <div className="mx-auto grid justify-center gap-4 sm:grid-cols-2 md:max-w-[64rem] md:grid-cols-3">
          <div className="relative overflow-hidden rounded-lg border bg-background p-2">
            <div className="flex h-[180px] flex-col justify-between rounded-md p-6">
              <Image 
                src={MondayIcon}
                alt="monday.com!"
                height={12}
                width={12}
                className="h-12 w-12 fill-current"
              />
              <div className="space-y-2">
                <h3 className="font-bold">Monday</h3>
                <p className="text-sm text-muted-foreground">
                  Use monday.com to build chatbots, add and delete documents, and see usage
                </p>
              </div>
            </div>
          </div>
          <div className="relative overflow-hidden rounded-lg border bg-background p-2">
            <div className="flex h-[180px] flex-col justify-between rounded-md p-6">
              <Image 
                  src={SlackIcon}
                  alt="slack.com!"
                  height={12}
                  width={12}
                  className="h-12 w-12 fill-current"
                />
              <div className="space-y-2">
                <h3 className="font-bold">Slack</h3>
                <p className="text-sm text-muted-foreground">
                  Deploy, chat and interact with your chatbots via an easy-to-use slack app.
                </p>
              </div>
            </div>
          </div>
          <div className="relative overflow-hidden rounded-lg border bg-background p-2">
            <div className="flex h-[180px] flex-col justify-between rounded-md p-6">
              <Image 
                    src={FileFolder}
                    alt="File folder"
                    height={12}
                    width={12}
                    className="h-12 w-12 fill-current"
                  />
              <div className="space-y-2">
                <h3 className="font-bold">Files</h3>
                <p className="text-sm text-muted-foreground">
                  Upload PDFs, text and word documents and CSVs in Monday that can be interacted with in Slack
                </p>
              </div>
            </div>
          </div>
          <div className="relative overflow-hidden rounded-lg border bg-background p-2">
            <div className="flex h-[180px] flex-col justify-between rounded-md p-6">
              <Image 
                      src={Checkmark}
                      alt="Checkmark"
                      height={12}
                      width={12}
                      className="h-12 w-12 fill-current"
                    />
              <div className="space-y-2">
                <h3 className="font-bold">Sources Included</h3>
                <p className="text-sm text-muted-foreground">
                  Every answer comes with accompanying sources to easily validate and dig deeper when needed.
                </p>
              </div>
            </div>
          </div>
          <div className="relative overflow-hidden rounded-lg border bg-background p-2">
            <div className="flex h-[180px] flex-col justify-between rounded-md p-6">
              <Image 
                src={UserAdoption}
                alt="User adoption"
                height={12}
                width={12}
                className="h-12 w-12 fill-current"
              />
              <div className="space-y-2">
                <h3 className="font-bold">Adoption</h3>
                <p className="text-sm text-muted-foreground">
                  Built on top of common apps. No need to add additional apps to your workflow.
                </p>
              </div>
            </div>
          </div>
          <div className="relative overflow-hidden rounded-lg border bg-background p-2">
            <div className="flex h-[180px] flex-col justify-between rounded-md p-6">
              <Image 
                  src={Trend}
                  alt="Trending"
                  height={12}
                  width={12}
                  className="h-12 w-12 fill-current"
                />
              <div className="space-y-2">
                <h3 className="font-bold">Common Trends</h3>
                <p className="text-sm text-muted-foreground">
                  Identify common questions being asked and ensure answers given are correct.
                </p>
              </div>
            </div>
          </div>
        </div>
        <div className="mx-auto text-center md:max-w-[58rem]">
          <p className="leading-normal text-muted-foreground sm:text-lg sm:leading-7">
            YakBots is constantly adapting to the current advancements and best practices in the world of AI.
          </p>
        </div>
      </section>
    </>
  )
} 

