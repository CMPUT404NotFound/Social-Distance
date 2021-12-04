no more base64 encoding, just unnecessary work. replace id: link's "/" with "-" so its url safe. 
(URL length is somewhat unlimited in this context i think)


foreign data needed:
## Author
+ fetch all foreign authors of a paricular node, api/nodes/otherNodeName/authors
+ fetch all foreign authors of all known nodes, api/ndoes/authors
## Following
+ follow a foreign user PUT api/author/{otherserver.com-service-author-foreignAuthorId}/followers/ouruserId
    + sends request to other if the first id's domain isn't ours.
    + just added it to our database otherwise
    + !!! regardless who's server it belongs to, also add to "Following" model, for querying who our user is following.
    
    - parsing: check item after 'author', use urllib.parse on item
        if netloc exists, just check the netloc to see if it is the same as ours, if so return parsed short id  

        if not return parsed long id to foreign site
        
        else: just treat it as a normal id, return islocal=false and just id
    
    - following only need to parse author, for PUT
    - GET should not be called from our own front end
    - !!! DELETE should be just called normally, no need to attach the full link id
+ needs a api to get a list of friends of a particular author. 
    B is A's friend if B is in A's follower table, and B is also in A's following table.
+ when our own PUT is called, push an inbox item indicating the follow

## Post
+ POST/PUT/DELETE should be called normally, ie, just POST api/author/\<id>/posts/\<postid\>/. Since we can't create/update otherservers
+ GET(hack in coming)
    + Gets the a particular post from either our server or a foreign server
    + Lets stuff the link in like so?
        GET api/author/\<some_id>/posts/{server.com-service-author-\<author_id>-posts-\<post_id>}/
        (\<some_id> - this id should only be checked if post id not a link)
    
    - parsing:
        parse the item after posts with urllib.parse
        if item is valid url, ie, notloc is not empty
            if netloc is ours -> return parsed short id for post
            else return parsed long id to the other server
        else just return id
        
    + only return if the post if public, or to friends if the post is friends only. 
    + Get author/id/posts/ should not return any unlisted posts
    + Get author/id/posts/ can return any posts, including unlisted ones.
    
+ On creating post via POST /posts/ or PUT /posts/\<postid>
    if the post is friends only, push this post to every friends' inbox, including foreign author that are friends.
## Comments
+ For both GET and POST, api/author/\<authorId>/posts/{server.com-service-author-\<authorID>-posts-\<postId>}/comments 
should GET and POST to both local and foreign server.   
(the first authorId only needs to be correct if the post id points to local site)
    
    -parsing: parsed the same way as post, described above.
    
## Likes
+ to like another comment/posts, regardless foreign or local, attach the like json body described as the docs,
do POST api/author/{site.com-service-author-\<authorId>-inbox}
- parsing: parse the same way as Author
GET list of likes for post:  GET api/author/\<some_id>/posts/{server.com-service-author-\<author_id>-posts-\<post_id>}/likes
similar to posts
GET list of for comment: GET api/author/\<some_id>/posts/\<some_id>/commments/{server.com-service-author-\<author_id>-posts-\<post_id>-comments-\<commentId>}/likes
author and post id are only checked if the comment id is for our site
GET api/author/\<id>/likes, see Author.
## Inbox
+ only DELETE and POST likes should be called by front end
    + DELETE should be called normally
    + post and follow is handled automatically in backend.
    
    
## Github
something along the lines of api/author/id/github for the current user's github activities.
