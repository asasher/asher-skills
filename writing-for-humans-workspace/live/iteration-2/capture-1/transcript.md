# Team invitations

Thread: 1e3a5b48-595f-47a3-8167-a3d4c79a67d3

## 1. user (runner kickoff)

Message: 2a188933-5d71-4c46-9fe9-cc28f822ad33 · 2026-09-17T11:29:13.870Z

I maintain a small team-management app. Sometimes people get two invitation emails when they double-click Invite. The frontend sends POST /invites for each click, and the server creates an invite and sends an email for every request. Clients also retry after timeouts.

I want to talk through how invitations and resends should work before implementing anything. Should we debounce the button or fix this on the server?

Use $writing-for-humans and $unslop.


## 2. assistant

Message: assistant:msg_0a5d1a50a95fe53b016aabcf0f787c87d0a04b6ec8c848ba9f · 2026-09-17T11:29:20.292Z

I'll use the writing-for-humans and unslop skills to talk through the behavior before we touch code.


## 3. assistant

Message: assistant:msg_0a5d1a50a95fe53b016aabcf15063887d0bdac16a6caa2e454 · 2026-09-17T11:29:38.221Z

Fix this on the server. I'd also disable Invite while a request is in progress, but debouncing only catches clicks close together. It won't protect against timeout retries or two teammates inviting the same person.

I'd start with this behavior:

| Situation | Server behavior |
|---|---|
| First invitation | Create a pending invite and queue an email. |
| Another Invite for the same team and email while it's pending | Return the existing invite without sending another email. |
| Retry after a timeout | Return the result of the original operation. |
| Explicit Resend | Queue another email for the existing invite, subject to a cooldown. |
| Person already belongs to the team | Return "Already a member" without sending an invitation. |

Two server protections cover different problems.

**Request idempotency** handles retries. The client gives each intended action an idempotency key and reuses it when retrying. The server remembers the result for that key. Reusing a key with different inputs should fail.

**A database constraint** prevents multiple pending invites for the same team and normalized email address. You need this even with idempotency keys, because separate clicks or separate people can produce different keys. A "check whether one exists, then insert" sequence alone can race.

I'd make Resend an explicit action with its own idempotency key and a server-enforced cooldown, perhaps 60 seconds. A timed-out resend can then be retried without requesting another email. For an unexpired invite, I'd keep the same link and expiry so earlier emails remain usable. Expired invites need a deliberate renewal policy.

The email handoff needs care too. Save the invite and a durable email job in the same database transaction. Otherwise a crash can leave an invite without an email, or a retry can send twice. The worker should use the email provider's idempotency support if available: a timeout after the provider accepts an email still leaves delivery uncertain.

My default would be: clicking Invite again shows "Invitation already pending" with a separate Resend button. Does that match what your team expects, or do they currently use Invite again to mean "send another email"?

## 4. user

Message: c63d14ca-9e00-480a-9d8a-227e78d540ed · 2026-09-17T11:35:04.904Z

I would like to do something similar to what GitHub does, where you can still resend an invite and invites just have an expiration date. It's just that we should not be resending invites accidentally

## 5. user

Message: 1e63bd26-28b2-4500-905c-60e698e69fc6 · 2026-09-17T11:35:20.685Z

And if the user accepts an invite and then accepts another invite because he found a duplicate email, then that should be handled gracefully

## 6. assistant

Message: assistant:msg_0a5d1a50a95fe53b016aabd0755d9487d0b45fe0d3017a0ab2 · 2026-09-17T11:35:25.931Z

Yes. I'd treat Invite and Resend as separate actions, with retries safe for both.

An invitation has an expiration date. Clicking Invite creates it and requests the first email. If a pending, unexpired invitation already exists for that team and email, the server returns it without sending another email. The UI shows its expiry and a Resend button.

Clicking Resend deliberately requests another email. I'd keep the same link and expiration date, so resending doesn't quietly extend access. Once the invite expires, the UI offers "Send new invitation" and the old link stays invalid.

To prevent accidental sends:

- Disable the button while its request is running.
- Give each intended action an idempotency key. Double-clicks and timeout retries reuse that key, so the server processes the action once.
- Enforce a short resend cooldown on the server, perhaps 60 seconds, to catch duplicate requests with different keys.
- Enforce one pending invitation per team and email in the database, including concurrent requests.

I'd apply the cooldown after the initial email too, so an immediate Resend can't produce a second email. After it ends, another deliberate resend is allowed.

That gives you expiring invitations and an explicit way to send a reminder, while repeated clicks and retries don't request extra emails. The email worker also needs duplicate protection at the provider handoff, since a provider timeout can happen after it has accepted the email.

## 7. assistant

Message: assistant:msg_0a5d1a50a95fe53b016aabd0b2348c87d0b1d28979c271e7ca · 2026-09-17T11:36:24.239Z

Agreed. Accepting an invite should also be safe to repeat.

For the same signed-in account:

- **Already accepted this invite:** show "You're already a member" and offer to open the team.
- **Accepted another invite to the same team:** show the same result. Don't create another membership or change their role.
- **No longer a member:** an old accepted invite must not let them rejoin. They need a new invitation.

The server should check that the signed-in account matches the invitation recipient. A forwarded link shouldn't give someone else the "already a member" success response.

I'd enforce one membership per team and account in the database, and accept the invite and create that membership in one transaction. That covers two acceptance requests arriving at the same time.

For duplicate emails containing the same link, the second click simply takes the person back to their team. Older duplicate invites with different links should behave just as gracefully if that person is still a member.
