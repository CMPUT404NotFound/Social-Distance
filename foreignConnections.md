

## On handling foreign connections / nodes
---
+ Our frontend is only usable if a local user is logged in, so lets use the login token granted to verify if a incoming connection is from our own frontend.
    + backend server green lights most incoming request from our own client
    + if a operation needs further auth, like deleting post, then check if this token belongs to the owner of the post.

### There should be a *Node* django model:  

+ Node:
    + Link, (the link to the other server for requests to be sent)
    + allowIncoming, bool, (allow incoming requests?)
    + allowOutgoing, bool, (allow/block access the this remote server?)
    + authRequiredIncoming, bool, (does this node need basic to access this server)
    + authRequiredOutGoing, bool,  ...
        + incoming username/password
        + outgoing username/password

So for nodes that needs authentication, `Authorization: Basic userid:password`,
if auth is not required, then when handling incoming/outgoing requests its just a simple black/white list via `allowIncoming` & `allowOutgoing`.

Hanlding of incoming requests should be done in the class `TokenAuth` (maybe rename this), or perhaps a seperate Authentication class. Outgoing requests should be checked in `utils.requests.py`, so check if the outgoing request is allowed, if auth is to be added etc.  

