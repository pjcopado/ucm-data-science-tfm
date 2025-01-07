import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { MantineProvider } from '@mantine/core'
import Head from 'next/head'
import { NotificationsProvider } from '@mantine/notifications'
import {  QueryClient,  QueryClientProvider } from '@tanstack/react-query'
import Layout from '../layout/layout'

const queryClient = new QueryClient();

export default function Home({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>My own ChatGPT</title>
        <meta name="viewport" content="minimum-scale=1, initial-scale=1, width= device-width"></meta>
      </Head>
      <MantineProvider
        withGlobalStyles
        withNormalizeCSS
        theme={{
          colorScheme: 'light'
        }}
      >
        <NotificationsProvider>
          <QueryClientProvider client={queryClient}>
              <Layout>
                  <Component {...pageProps} />
              </Layout>
          </QueryClientProvider>
        </NotificationsProvider>
      </MantineProvider>
    </>
  )
}