# Trotto Go Links

> **Trotto is an active, supported product.** For go links at your company, use the hosted version at
> [trot.to](https://www.trot.to). It's free for up to 10 users, with Chrome and Firefox extensions, Google and
> Microsoft sign-in (Okta and OneLogin on Enterprise), a Slack app, and SOC 2 Type II.
> [Get started](https://www.trot.to/getting-started) · [Pricing](https://www.trot.to/pricing) · [Docs](https://docs.trot.to)

This repository is the **legacy open-source edition** of Trotto's go links server. It is no longer maintained.
The hosted Trotto product is separate and is still actively developed.

## About this repository

Trotto started in 2017. In April 2025 we stopped maintaining this open-source edition. The reasons
were Chrome's Manifest v3 changes, the ongoing maintenance cost, and our roadmap for the hosted product. For this
repository, that means:

- No new features will be added
- No bug fixes will be implemented
- Issues and pull requests will be closed
- The *open-source* browser extension repository has been taken down. If you still run it, Chrome decides how long
  it will keep allowing private Manifest v2 extensions.

**This applies only to the open-source edition.** The hosted Trotto browser extension is maintained and Manifest v3
compliant, and it's available on the
[Chrome Web Store](https://chromewebstore.google.com/detail/trotto-go-links/nkeoojidblilnkcbbmfhaeebndapehjk) and
[Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/trotto-go-links/).

## Moving to hosted Trotto

If you run this project yourself, we'd love for you to try hosted Trotto. You also get:

- An updated UI
- SSO integration
- Admin controls, including analytics
- A Slack app
- A Manifest v3 browser extension
- SOC 2 Type II audits
- "Featured" go links

Questions about moving over? Email [help@trot.to](mailto:help@trot.to).

We're grateful for everything we learned maintaining this project, and thank you for being part of this journey.

## Features

This [go links](https://www.trot.to/go-links) solution has run in production continuously since 2017, and it is
still the core of [Trotto](https://www.trot.to).

Trotto provides all the baseline functionality you'd expect from a go links solution, including the ability to
create, use, and modify go links that are shared with your organization—and with nobody else.

Trotto also includes powerful features above and beyond a basic go links implementation, including a searchable go
links directory, a browser extension that makes go links work instantly,
and programmatic links, which are go links containing placeholders that map onto the destination
URL (ex: `go/gh/%s` pointing to `https://github.com/my_org/%s`).
