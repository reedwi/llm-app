import { Button, buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import Image from "next/image";
import Link from "next/link";

const InstallPage = async ({
  params
}: {
  params: { accountId: string }
}) => {
  return (
    <div className="flex items-center justify-center">
      <div className="justify-between space-y-4">
      <Separator />
        <h1 className="text-xl">Let&apos;s get you setup with YakBot!</h1>
        <p>Want to just use the Slack app?<br/>
        Head down to Step 11 and just follow the Slack install<br/>
        You will instantly get access to GPT-4 and the ability to chat against documents uploaded via Slack
        </p>
        <Separator />
        <div className="justify-between space-y-2">
          <h2>Step 1</h2>
          <p>
            Ensure you have a workspace created in monday.com where you want to install the monday boards.<br />
            This does not specifically need to be a new workspace, nor does it need to only be used for this application.<br /> To learn more
            about workspaces head <a className="text-orange" target="_blank" href="https://support.monday.com/hc/en-us/articles/360010785460-The-Workspaces" rel="noopener noreferrer">here.</a><br /><br />
            Do you need a monday.com account? Click <a className="text-orange" target="_blank" href="https://auth.monday.com/users/sign_up_new/?utm_source=Partner&utm_campaign=oboagency#soft_signup_from_step" rel="noopener noreferrer">here</a> to get a 7 day free trial!
          </p>
        </div>
        <Separator />
        <div className="justify-between space-y-2">
          <h2 >Step 2</h2>
          <p>
            Install the app in Monday following the below button.
          </p>
          <Button asChild>
            <a target="_blank" href={`https://auth.monday.com/oauth2/authorize?client_id=b11f269b50b32a2083d401171ff5e5fb&response_type=install`} rel="noopener noreferrer">Install in Monday</a>
          </Button>
        </div>
        <Separator />
        <div className="justify-between space-y-2">
          <h2 >Step 3</h2>
          <p>
            Authorize the app in Monday following the below link. This can take 3-10 seconds to fully process. <br/>
            You will use this tab to complete the configration of the app. Please wait until you get to the screen <br/>
            that is shown in Step 4. <br /><br />

          </p>
          <Button asChild>
            <a target="_blank" href={`https://auth.monday.com/oauth2/authorize?client_id=b11f269b50b32a2083d401171ff5e5fb&state=${params.accountId}`} rel="noopener noreferrer">Authorize Monday</a>
          </Button>
          <br/><br/><b>Troubleshooting</b><br />
            If you are not redirected to the screen shown in Step 4,
            please append <br />&quot;/apps/installed_apps/10088167&quot; to the end of your monday url. <br /><br />
            Will look something like &quot;https://testcompany.monday.com/apps/installed_apps/10088167&quot;, <br/>
            &quot;testcompany&quot; will be dynamic based
            on your monday account so this will be different for you
        </div>
        <Separator />
        <div className="justify-between space-y-2">

            <div className="justify-between space-y-2"><h2 >Step 4</h2><h3>Click on Use App</h3>
            <img src="https://images.tango.us/workflows/ef5e24c8-c9d0-45a0-9e3a-a6dfe0d1f548/steps/5e49cbf8-c6b5-4adf-8ce6-a9db6ccdf330/c324c498-1223-4863-b5e9-0fc5e1c480fb.png?fm=png&crop=focalpoint&fit=crop&fp-x=0.2799&fp-y=0.4645&fp-z=1.7896&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&mark-x=123&mark-y=323&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz0xMjYmaD02MCZmaXQ9Y3JvcCZjb3JuZXItcmFkaXVzPTEw" width="600" alt="Click on Use App" />
            </div>
            <Separator />

            <div className="justify-between space-y-2"><h2 >Step 5</h2><h3>Click in the &quot;Choose a workspace&quot; dialog</h3>
            <img src="https://images.tango.us/workflows/ef5e24c8-c9d0-45a0-9e3a-a6dfe0d1f548/steps/5614b858-f937-4d53-958f-357dcabd0011/2ae29263-4122-4683-9bc3-e2b1cb34ca57.png?fm=png&crop=focalpoint&fit=crop&fp-x=0.5000&fp-y=0.5116&fp-z=1.0178&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&mark-x=11&mark-y=7&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz0xMTc5Jmg9NzM4JmZpdD1jcm9wJmNvcm5lci1yYWRpdXM9MTA%3D" width="600" alt="Click on dialog" />
            </div>
            <Separator />

            <div className="justify-between space-y-2"><h2 >Step 6</h2><h3>Type and find the workspace where you want to install the boards. <br/>For new accounts please just select &quot;Main&quot;</h3>
            <img src="https://images.tango.us/workflows/ef5e24c8-c9d0-45a0-9e3a-a6dfe0d1f548/steps/e93c57e9-7d61-410e-b275-1ce8a1f1d72d/3e52aed4-6985-4a77-83ac-912f520ab366.png?fm=png&crop=focalpoint&fit=crop&fp-x=0.5000&fp-y=0.5116&fp-z=1.0178&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&mark-x=11&mark-y=7&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz0xMTc5Jmg9NzM4JmZpdD1jcm9wJmNvcm5lci1yYWRpdXM9MTA%3D" width="600" alt="Type and find the workspace we made in a prior step" />
            </div>
            <Separator />

            <div className="justify-between space-y-2"><h2 >Step 7</h2><h3>Click on Add app</h3>
            <img src="https://images.tango.us/workflows/ef5e24c8-c9d0-45a0-9e3a-a6dfe0d1f548/steps/2ec9d386-337e-476e-aea1-17d037c5e2d1/b47dde24-4475-45ee-9154-803d90920288.png?fm=png&crop=focalpoint&fit=crop&fp-x=0.5319&fp-y=0.3913&fp-z=2.7255&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&mark-x=491&mark-y=321&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz0yMTkmaD0xMDYmZml0PWNyb3AmY29ybmVyLXJhZGl1cz0xMA%3D%3D" width="600" alt="Click on Add app" />
            </div>
            <Separator />

            <div className="justify-between space-y-2"><h2 >Step 8</h2><h3>Click on Chatbots, if not already directed there</h3>
            <img src="https://images.tango.us/workflows/ef5e24c8-c9d0-45a0-9e3a-a6dfe0d1f548/steps/d9c2e626-b864-482a-b6ad-48360c0f0b5e/c84eb8da-aabc-4ade-93bc-56e661f6b7e4.png?fm=png&crop=focalpoint&fit=crop&fp-x=0.1139&fp-y=0.3527&fp-z=2.2070&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&mark-x=99&mark-y=341&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz00MDUmaD02NyZmaXQ9Y3JvcCZjb3JuZXItcmFkaXVzPTEw" width="600" alt="Click on Chatbots, if not already directed there" />
            </div>
            <Separator />

            <div className="justify-between space-y-2"><h2 >Step 9</h2><h3>Click on Integrate</h3>
            <img src="https://images.tango.us/workflows/ef5e24c8-c9d0-45a0-9e3a-a6dfe0d1f548/steps/9fec1507-af56-4cf2-9896-6d3e2b80bbfb/f7554807-3e2e-4d91-894e-28c1c3bb4070.png?fm=png&crop=focalpoint&fit=crop&fp-x=0.8258&fp-y=0.1213&fp-z=3.0486&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&mark-x=503&mark-y=245&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz0xOTQmaD02NCZmaXQ9Y3JvcCZjb3JuZXItcmFkaXVzPTEw" width="600" alt="Click on Integrate" />
            </div>
            <Separator />

            <div className="justify-between space-y-2"><h2 >Step 10</h2><h3>Confirm there are 4 integration recipes added</h3>
            <p>Please allow up to 5 minutes for the integration recipes to populate. It can be a little slow on initial install of the app</p>
            <img src="https://images.tango.us/workflows/ef5e24c8-c9d0-45a0-9e3a-a6dfe0d1f548/steps/72c57a5b-ba15-4947-a8c8-57c57ff40bdd/3ec7b89e-4b85-44bb-a861-abdd0d61c249.png?fm=png&crop=focalpoint&fit=crop&fp-x=0.5000&fp-y=0.5816&fp-z=1.0178&w=1200&border=2%2CF4F2F7&border-radius=8%2C8%2C8%2C8&border-radius-inner=8%2C8%2C8%2C8&mark-x=11&mark-y=114&m64=aHR0cHM6Ly9pbWFnZXMudGFuZ28udXMvc3RhdGljL2JsYW5rLnBuZz9tYXNrPWNvcm5lcnMmYm9yZGVyPTYlMkNGRjc0NDImdz0xMTc5Jmg9NjMyJmZpdD1jcm9wJmNvcm5lci1yYWRpdXM9MTA%3D" width="600" alt="Confirm there are 4 integration recipes added" />
            </div>
            <Separator />
        </div>
        <div className="justify-between space-y-2"><h2 >Step 11</h2>
          <h3>
            Install the app in Slack following the below button<br/>
            For &quot;Where should YakBot post?&quot; select Slackbot
          </h3>
          <Button asChild>
            <a target="_blank" href={`https://slack.com/oauth/v2/authorize?client_id=14167971015.5153442767168&scope=app_mentions:read,channels:history,channels:read,chat:write,chat:write.customize,commands,files:read,files:write,im:history,im:read,im:write,incoming-webhook,links:read,links:write,users:read,users:read.email&user_scope=chat:write&state=${params.accountId}`} rel="noopener noreferrer">Install in Slack</a>
          </Button>
        </div>
        <Separator />
        <div className="justify-between space-y-2"><h2 >Step 12</h2>
          <h3>
            You are now setup to begin using and building your chatbots. <br />In the monday YakBot folder
            you will find documentation on how to use YakBot. <br />
            We recommend starting with <a className="text-orange" target="_blank" href={`https://app.tango.us/app/workflow/Managing-Chatbots-and-Documents--A-Step-by-Step-Tutorial-1a9e0e36f85a494d851f957540513dbc`} rel="noopener noreferrer">&quot;Managing Chatbots and Documents: A Step-by-Step Tutorial&quot;</a>  and <a className="text-orange" target="_blank" href={`https://app.tango.us/app/workflow/Navigating-Slack-App-64e25ac3ce1e43199bcb2a03b1cb125e`} rel="noopener noreferrer">&quot;Navigating the Slack App&quot;</a> to get started.<br />
            You can also find these docs and additional resources in the Docs page of the app <Link href={`/${params.accountId}/docs`} className="text-orange">here</Link>
          </h3>
        </div>
        <Separator />
        <div className="justify-between space-y-2">
        </div>
      </div>
    </div>
  )
} 

export default InstallPage;
