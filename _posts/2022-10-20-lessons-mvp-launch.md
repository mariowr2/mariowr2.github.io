---
layout: post
section-type: post
title: Lessons from a successful(ish) mvp startup launch
category: startups
tags: ["Startup", "MVP"]
---

In August of 2022 we launched the Evotrux 2.0 MVP. The new shipment-matching platform was built from the ground-up after a couple years of learning what customers actually wanted through Evotrux 1.0.  
After a couple funding rounds, myself and a couple more people were hired to build the new version of the Evotrux platform along with the remaining team after a pandemic-induced downturn period. This (not so brief) blog post is my attempt at writing down what I wish I’d known before this project. I hope this is helpful or at least somewhat entertaining :) . Here we go.

[More about Evotrux](https://www.evotrux.com).

## TL; DR

- Know your team in person. Especially if your team is remote.
- If your dev team is new, agree on a coding standard as soon as you can.
- IAC, Environment Parity and solid CI/CD processes are a must.
- Develop the least you can and don’t be afraid to say ‘No’ and ‘what if…?’ to business.
- Some degree of observability and monitoring of your application should be implemented pre-launch.
- Don’t overwork yourself and lookout for your team.
- Launching the MVP is only half the battle – be mentally prepared for the work post-launch.
- Build and trust your team. Trust yourself.

## The goal

The dev team’s objective was to ship an MVP with the core features of what Evotrux is: matching shippers with carriers, enabling them to negotiate prices on shipments, ask questions, email notifications and so on. The MVP needed to ship out as a stable product with good performance and better UX. The working software needed to be delivered as soon as possible while being careful to ensure that tech debt did not make us too slow post-launch, as feature development would continue pretty soon after launching. Though the project had started since December 2021, it only received full-time attention from several developers until April 2022 – and most of the features were developed from that point onwards. The launch date was planned for the second week of August 2022.

The following are a series of key points that I believe were most impactful on the Evotrux 2.0 MVP being a success from a development standpoint. Let’s jump right into it.

### 1. Know your team

Meeting the team changed the course of the MVP. Evotrux is a largely remote company that had gone through significant staff changes before the project began; meaning that most of the people had never been in the same room prior to starting the project. To address this and get some serious MVP planning done, Evotrux leadership setup a week of planning meetings at a co-working space. Through these meetings some key events happened:

- The team spent time together and formed personal bonds. The free beer at the co-working space made everyone happy.
- We defined the agile “flavour” that the development team would be following. Business now understood what to expect when working with us to get features out the door.
- The whole Evotrux team listened and debated on what we wanted to build and why it was important to build it. Being new to the company, listening to these discussions brought us closer to the domain of logistics. The new software team learned about our value proposition and who our users are. I believe that this introduction to the domain of logistics was crucial in boosting our ability to understand requirements later.
- The dev team was able to guide the discussion around what was technically feasible given the amount of time and to manage business expectations.
- Most importantly, the dev team understood the urgency of and the amount of work that was ahead of us.

Where it not for this series of meetings I don’t think I would be writing this blog post today. Remote communication is hard. Communicating a product/vision (both in person and remote) and planning for it also hard. Put those two together and efficiently communicating the plan and vision to a remote, mostly newly-formed team becomes a real challenge. Remote work is pretty cool, and so are in-person meetings.

### 2. Agree on a coding standard

As a newly formed dev team we all had different ideas of how our code should be structured. Should we lean heavily on the framework’s way of doing things? Should we go full [DDD](https://en.wikipedia.org/wiki/Domain-driven_design)? A mix of both? These are structural questions, and not being on the same page led to long and protracted discussions at code review time. Through a bit of pair programming and passionate discussion we managed to agree on what we wanted our code to look like. Once we figured this out, the speed at which we worked and the quality of experience increased. New teams should discuss their ideas and agree on coding standards as soon as there is enough code for a couple of concrete implementations to compare.

### 3. IAC, Environment Parity and solid CI/CD process is a must

[Environment parity](https://12factor.net/dev-prod-parity) and a CI/CD are well established software engineering practices. [IAC](https://en.wikipedia.org/wiki/Infrastructure_as_code) (Infrastructure as code) is also quickly becoming a standard in the cloud world. I would like to briefly describe how these three played together to make our dev lives slightly less busy. IAC and environment parity allowed us to deploy our internal QA version of the system and prod version of the system very early on. Thanks to IAC, the systems were nearly identical from end to end, which made the QA environment very useful to find bugs and misunderstandings in requirements. Since each environment is almost identical, code becomes (almost) environment-agnostic, which makes it harder to introduce environment-specific problems. Another benefit is that CI/CD pipelines only need to be written once: since each environment has the same components and steps to deploy, you only need to ensure your CI/CD pipeline can take in different secrets, ARNs and so on per environment. I believe ideally these three components must be built at the same time as the main components of any system (if not before). Deploy as early as possible and invest the time in having a solid CI/CD process. The time investment quickly pays off when the time crunch arrives down the line.

### 4. Do the least you can get away with

This one is straightforward and is already a golden rule when building MVPs. Doing less allows developers to focus on the core features. When the product offering is well defined, quality wins over quantity.

#### Saying ‘No’ and ‘what if…?’

A key skill for developers planning features with business is to be able to say ‘No’ when needed. In the context of building software against time, not saying no when required can make dev teams commit to features in unrealistic timelines, which further delays the project. Be aware that often non-tech processes happen based on development timelines (for example running a marketing campaign around the launch date), so therefore optimistic or inaccurate planning often affects more areas beyond the dev team. On happy days, resist the urge to optimistically over-promise what can be done.

Before we get to planning timelines, the effort to boil down requirements into what is absolutely needed is also key. Shed as much as possible. Through no fault of their own, business teams lacking technical knowledge can easily underestimate time and effort required to develop features. When fleshing out features with business, being able to find alternative paths is also well worth the effort. For larger features/components proposed by business, I suggest thinking of a way to reduce the technical effort and time investment. If there is such a way, propose it. A dialog often ensues where devs and business can arrive to a middle point where what’s delivered is realistic for both sides. Often a small change in the plan can make development much faster. Time in a start-up's journey is a precious resource that must be carefully guarded. In order to protect this resource it is key for dev teams to be involved in planning beyond just taking requirements.

### 5. Observability and Monitoring

It is hard to overstate how useful investing time in both of these became post-launch. Lacking the time to build an internal dashboard for the business team to monitor the application’s state, we opted for a quick n’ dirty slack bot that would relay key application events along with metadata (such as shipments posted, quotes created, quotes expired etc.) to our slack in real time. This slack bot proved a useful tool to gauge system activity at any moment.

Being able to observe events in real time was especially helpful on the days post-launch, as the whole company was able to see all system activity and respond quickly to customer service needs. Besides these company-wide advantages, I found that as developer, knowing about key events happening motivated me to keep working – someone out there was using our software. I think the takeaway here is that teams should set aside a small amount of time to think about how non-technical team members will stay informed on what is happening in the system on launch. Depending on time availability, you might be able to build something far better than a slack bot!

#### Error Monitoring

Alongside our slack bot observability “hack”, having error monitoring gave us the ability to know about errors and user confusion in real time. We used [Sentry](https://sentry.io/welcome/) – which was extremely useful to setup (I highly recommend checking them out). Given the scale of our launch (we were expecting up to a hundred users in the first couple weeks) , we configured Sentry to send a slack message every-time any error (handled or unhandled) came up on our backend. The plan was to make it as easy as possible to fix any error that came up on launch without having to dig through logs to piece information from a request.

Out of the box, every error reported by Sentry came with a stack trace, a bit of log output and most importantly metadata about the request (i.e which user made the request, what time, which OS etc.). This made it very straightforward to address problems as well as to identify whenever a user was having trouble. For example, plenty of our users failed to verify their emails after creating their account. Before they even reached out to us asking why they could not log in, we were already sending personalized messages explaining how to solve their issue. As a new app it is important to earn user trust. Being able to quickly identify problems and respond to them shows users that the team behind the application is competent and that we care.

### 6. Overworking

Building against time is as much as physical effort as mental effort. With solid planning on your side, the dev team should have well defined (and well understood!) goals for the short term with as little distraction as possible. Even with solid planning, I found it very easy to fall into anxiety about being able to deliver the work for the day/week/sprint/project. In my experience, this often resulted in working extra. Working extra hours is no doubt part of the startup experience but as developers it is our responsibility to identify the point where mental energy is low enough that we risk lowering the quality of our work. In this low energy state, it is usually much easier to introduce bugs and spend hours going in circles when something goes wrong – only to solve the problem the next morning with a fresh brain. Work extra hours when you must, but remain attentive to the point where you stop moving forward and stop there.

### 7. Visualize the effort ahead as constant

It's important to think of the days/weeks/months' worth of work as a constant effort. If building an MVP were a race, launching the product to customers is only half the race. After launch, you will have to deal with customers, troubleshoot problems the moment they arise, gather data for business and so on.

Depending on your role within the team, interruptions will become much more frequent. This is why I believe it's important to remind ourselves through the pre-launch phase that building the software is only the first chapter and that more work comes after. Visualizing the effort as a pyramid is tempting to motivate hard-working in order to “just get to launch”; but this approach can work against us once launch day arrives. Besides looking out to not overwork yourself, remember to lookout for your teammates. Ask teammates to take days off if you know they’ve worked extra hard through the week. Ask for a day off when you need a recovery day. Being aware that the same or more effort on the days post-launch is needed can help us manage our pace through not overworking prematurely.

### 8. Trust your team – and yourself

I left the most important one for last. Knowing you can rely on the people you work with can bring real peace of mind when working under pressure. To benefit from this, it's important to foster a team culture through every interaction. Be the person to build this trust: Be the first to reply to questions on slack, offer pair programming when someone is stuck, and get to know your teammates. Building software at scale is a team effort, and it pays to know and trust your team.

Finally, before you can build trust within a team, you must build trust within yourself. Know that the best way to learn is to do it – "It always seems impossible until it's done". Know that all we can do is try our best and that our best effort looks different every day.

### The End

That’s it. These are the things I knew before building Evotrux 2.0. I’m very thankful for the opportunity to have participated in this project and look towards the future with excitement for Evotrux. I hope this is useful to someone about to embark on a similar journey or that it can brings a smile to someone who went through a similar experience. Cheers!
