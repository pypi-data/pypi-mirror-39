# bklv2
bklv2 is a python library for [Backlog API version 2](https://developer.nulab-inc.com/docs/backlog/)
[(JP)](http://developer.nulab-inc.com/ja/docs/backlog).

## Install
~~~~
$ pip install bklv2
~~~~

## How to use
~~~~python
import bklv2

# make object.
bklv2api = bklv2.api( hostname="https://<spacename>.backlog.jp", apikey="apikey" )

# API method
# return : dict
prj = bklv2api.addProject( name = "testproject",
                           key = "TESTPROJECT",
                           chartEnabled = False,
                           subtaskingEnabled = False,
                           textFormattingRule = "markdown" )

print( type(prj) )          # >> <class 'dict'>
print( prj["projectKey"] )  # >> TESTPROJECT

# API method ( file-downloader )
# return : output file path
fp = bklv2api.getProjectIcon( projectIdOrKey=prj["id"]) )

print( type(fp) )           # >> <class 'str'>
print( fp )                 # >> ./space_img.png
~~~~

## API methods
| method | description |
|:------:|:------------|
| [getSpace](https://developer.nulab-inc.com/docs/backlog/api/2/get-space) | Returns information about your space. |
| [getRecentUpdates](https://developer.nulab-inc.com/docs/backlog/api/2/get-recent-updates) | Returns recent updates in your space. |
| [getSpaceLogo](https://developer.nulab-inc.com/docs/backlog/api/2/get-space-logo) | Returns logo image of your space. |
| [getSpaceNotification](https://developer.nulab-inc.com/docs/backlog/api/2/get-space-notification) | Returns space notification. |
| [updateSpaceNotification](https://developer.nulab-inc.com/docs/backlog/api/2/update-space-notification) | Updates space notification. |
| [getSpaceDiskUsage](https://developer.nulab-inc.com/docs/backlog/api/2/get-space-disk-usage) | Returns information about space disk usage. |
| [postAttachmentFile](https://developer.nulab-inc.com/docs/backlog/api/2/post-attachment-file) | Posts an attachment file for issue or wiki. Returns id of the attachment file.The file will be deleted after it has been attached. If attachment fails, the file will be deleted an hour later. |
| [getUserList](https://developer.nulab-inc.com/docs/backlog/api/2/get-user-list) | Returns list of users in your space.When the user has not set “lang”, the response will be null. |
| [getUser](https://developer.nulab-inc.com/docs/backlog/api/2/get-user) | Returns information about user.When the user has not set “lang”, the response will be null. |
| [addUser](https://developer.nulab-inc.com/docs/backlog/api/2/add-user) | Adds new user to the space.“Project Administrator” cannot add “Admin” user.You can’t use this API at backlog.com space. |
| [updateUser](https://developer.nulab-inc.com/docs/backlog/api/2/update-user) | Updates information about user.You can’t use this API at backlog.com space. |
| [deleteUser](https://developer.nulab-inc.com/docs/backlog/api/2/delete-user) | Deletes user from the space.You can’t use this API at backlog.com space. |
| [getOwnUser](https://developer.nulab-inc.com/docs/backlog/api/2/get-own-user) | Returns own information about user. |
| [getUserIcon](https://developer.nulab-inc.com/docs/backlog/api/2/get-user-icon) | Downloads user icon. |
| [getUserRecentUpdates](https://developer.nulab-inc.com/docs/backlog/api/2/get-user-recent-updates) | Returns user’s recent updates |
| [getReceivedStarList](https://developer.nulab-inc.com/docs/backlog/api/2/get-received-star-list) | Returns the list of stars that user received. |
| [countUserReceivedStars](https://developer.nulab-inc.com/docs/backlog/api/2/count-user-received-stars) | Returns number of stars that user received. |
| [getListOfRecentlyViewedIssues](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-recently-viewed-issues) | Returns list of issues which the user viewed recently. |
| [getListOfRecentlyViewedProjects](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-recently-viewed-projects) | Returns list of projects which the user viewed recently. |
| [getListOfRecentlyViewedWikis](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-recently-viewed-wikis) | Returns list of Wikis which the user viewed recently. |
| [getListOfGroups](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-groups) | Returns list of groups. |
| [addGroup](https://developer.nulab-inc.com/docs/backlog/api/2/add-group) | Adds new group.You can’t use this API at backlog.com space. |
| [getGroup](https://developer.nulab-inc.com/docs/backlog/api/2/get-group) | Returns information about group. |
| [updateGroup](https://developer.nulab-inc.com/docs/backlog/api/2/update-group) | Updates information about group.You can’t use this API at backlog.com space. |
| [deleteGroup](https://developer.nulab-inc.com/docs/backlog/api/2/delete-group) | Deletes group.You can’t use this API at backlog.com space. |
| [getStatusList](https://developer.nulab-inc.com/docs/backlog/api/2/get-status-list) | Returns list of statuses. |
| [getResolutionList](https://developer.nulab-inc.com/docs/backlog/api/2/get-resolution-list) | Returns list of resolutions. |
| [getPriorityList](https://developer.nulab-inc.com/docs/backlog/api/2/get-priority-list) | Returns list of priorities. |
| [getProjectList](https://developer.nulab-inc.com/docs/backlog/api/2/get-project-list) | Returns list of projects. |
| [addProject](https://developer.nulab-inc.com/docs/backlog/api/2/add-project) | Adds new project. |
| [getProject](https://developer.nulab-inc.com/docs/backlog/api/2/get-project) | Returns information about project. |
| [updateProject](https://developer.nulab-inc.com/docs/backlog/api/2/update-project) | Updates information about project. |
| [deleteProject](https://developer.nulab-inc.com/docs/backlog/api/2/delete-project) | Deletes project. |
| [getProjectIcon](https://developer.nulab-inc.com/docs/backlog/api/2/get-project-icon) | Downloads project icon. |
| [getProjectRecentUpdates](https://developer.nulab-inc.com/docs/backlog/api/2/get-project-recent-updates) | Returns recent update in the project. |
| [addProjectUser](https://developer.nulab-inc.com/docs/backlog/api/2/add-project-user) | Adds user to list of project members. |
| [getProjectUserList](https://developer.nulab-inc.com/docs/backlog/api/2/get-project-user-list) | Returns list of project members. |
| [deleteProjectUser](https://developer.nulab-inc.com/docs/backlog/api/2/delete-project-user) | Removes user from list project members. |
| [addProjectAdministrator](https://developer.nulab-inc.com/docs/backlog/api/2/add-project-administrator) | Adds “Project Administrator” role to user |
| [getListOfProjectAdministrators](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-project-administrators) | Returns list of users who has Project Administrator role |
| [deleteProjectAdministrator](https://developer.nulab-inc.com/docs/backlog/api/2/delete-project-administrator) | Removes Project Administrator role from user |
| [getIssueTypeList](https://developer.nulab-inc.com/docs/backlog/api/2/get-issue-type-list) | Returns list of Issue Types in the project. |
| [addIssueType](https://developer.nulab-inc.com/docs/backlog/api/2/add-issue-type) | Adds new Issue Type to the project. |
| [updateIssueType](https://developer.nulab-inc.com/docs/backlog/api/2/update-issue-type) | Updates information about Issue Type. |
| [deleteIssueType](https://developer.nulab-inc.com/docs/backlog/api/2/delete-issue-type) | Deletes Issue Type. |
| [getCategoryList](https://developer.nulab-inc.com/docs/backlog/api/2/get-category-list) | Returns list of Categories in the project. |
| [addCategory](https://developer.nulab-inc.com/docs/backlog/api/2/add-category) | Adds new Category to the project. |
| [updateCategory](https://developer.nulab-inc.com/docs/backlog/api/2/update-category) | Updates information about Category. |
| [deleteCategory](https://developer.nulab-inc.com/docs/backlog/api/2/delete-category) | Deletes Category. |
| [getVersionMilestoneList](https://developer.nulab-inc.com/docs/backlog/api/2/get-version-milestone-list) | Returns list of Versions/Milestones in the project. |
| [addVersionMilestone](https://developer.nulab-inc.com/docs/backlog/api/2/add-version-milestone) | Adds new Version/Milestone to the project. |
| [updateVersionMilestone](https://developer.nulab-inc.com/docs/backlog/api/2/update-version-milestone) | Updates information about Version/Milestone. |
| [deleteVersion](https://developer.nulab-inc.com/docs/backlog/api/2/delete-version) | Deletes Version. |
| [getCustomFieldList](https://developer.nulab-inc.com/docs/backlog/api/2/get-custom-field-list) | Returns list of Custom Fields in the project. |
| [addCustomField](https://developer.nulab-inc.com/docs/backlog/api/2/add-custom-field) | Adds new Custom Field to the project. |
| [updateCustomField](https://developer.nulab-inc.com/docs/backlog/api/2/update-custom-field) | Updates Custom Field. |
| [deleteCustomField](https://developer.nulab-inc.com/docs/backlog/api/2/delete-custom-field) | Deletes Custom Field. |
| [addListItemForListTypeCustomField](https://developer.nulab-inc.com/docs/backlog/api/2/add-list-item-for-list-type-custom-field) | Adds new list item for list type custom field.Only administrator can call this API if the option “Add items in adding or editing issues” is disabled in settings.Calling API fails if specified custom field’s type is not a list. |
| [updateListItemForListTypeCustomField](https://developer.nulab-inc.com/docs/backlog/api/2/update-list-item-for-list-type-custom-field) | Updates list item for list type custom field.Calling API fails if specified custom field’s type is not a list. |
| [deleteListItemForListTypeCustomField](https://developer.nulab-inc.com/docs/backlog/api/2/delete-list-item-for-list-type-custom-field) | Deletes list item for list type custom field.Calling API fails if specified custom field’s type is not a list. |
| [getListOfSharedFiles](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-shared-files) | Gets list of Shared Files. |
| [getFile](https://developer.nulab-inc.com/docs/backlog/api/2/get-file) | Downloads the file. |
| [getProjectDiskUsage](https://developer.nulab-inc.com/docs/backlog/api/2/get-project-disk-usage) | Returns information about project disk usage. |
| [getListOfWebhooks](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-webhooks) | Returns list of webhooks. |
| [addWebhook](https://developer.nulab-inc.com/docs/backlog/api/2/add-webhook) | Adds new webhook. |
| [getWebhook](https://developer.nulab-inc.com/docs/backlog/api/2/get-webhook) | Returns information about webhook. |
| [updateWebhook](https://developer.nulab-inc.com/docs/backlog/api/2/update-webhook) | Updates information about webhook. |
| [deleteWebhook](https://developer.nulab-inc.com/docs/backlog/api/2/delete-webhook) | Deletes webhook. |
| [getIssueList](https://developer.nulab-inc.com/docs/backlog/api/2/get-issue-list) | Returns list of issues. |
| [countIssue](https://developer.nulab-inc.com/docs/backlog/api/2/count-issue) | Returns number of issues. |
| [addIssue](https://developer.nulab-inc.com/docs/backlog/api/2/add-issue) | Adds new issue. |
| [getIssue](https://developer.nulab-inc.com/docs/backlog/api/2/get-issue) | Returns information about issue. |
| [updateIssue](https://developer.nulab-inc.com/docs/backlog/api/2/update-issue) | Updates information about issue. |
| [deleteIssue](https://developer.nulab-inc.com/docs/backlog/api/2/delete-issue) | Deletes issue. |
| [getCommentList](https://developer.nulab-inc.com/docs/backlog/api/2/get-comment-list) | Returns list of comments in issue. |
| [addComment](https://developer.nulab-inc.com/docs/backlog/api/2/add-comment) | Adds a comment to the issue. |
| [countComment](https://developer.nulab-inc.com/docs/backlog/api/2/count-comment) | Returns number of comments in issue. |
| [getComment](https://developer.nulab-inc.com/docs/backlog/api/2/get-comment) | Returns information about comment. |
| [deleteComment](https://developer.nulab-inc.com/docs/backlog/api/2/delete-comment) | Delete comment.User can delete own comment. |
| [updateComment](https://developer.nulab-inc.com/docs/backlog/api/2/update-comment) | Updates content of comment.User can update own comment. |
| [getListOfCommentNotifications](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-comment-notifications) | Returns the list of comment notifications. |
| [addCommentNotification](https://developer.nulab-inc.com/docs/backlog/api/2/add-comment-notification) | Adds notifications to the comment.Only the user who added the comment can add notifications. |
| [getListOfIssueAttachments](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-issue-attachments) | Returns the list of issue attachments. |
| [getIssueAttachment](https://developer.nulab-inc.com/docs/backlog/api/2/get-issue-attachment) | Downloads issue’s attachment file. |
| [deleteIssueAttachment](https://developer.nulab-inc.com/docs/backlog/api/2/delete-issue-attachment) | Deletes an attachment of issue. |
| [getListOfLinkedSharedFiles](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-linked-shared-files) | Returns the list of linked Shared Files to issues. |
| [linkSharedFilesToIssue](https://developer.nulab-inc.com/docs/backlog/api/2/link-shared-files-to-issue) | Links shared files to issue. |
| [removeLinkToSharedFileFromIssue](https://developer.nulab-inc.com/docs/backlog/api/2/remove-link-to-shared-file-from-issue) | Removes link to shared file from issue. |
| [getWikiPageList](https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page-list) | Returns list of Wiki pages. |
| [countWikiPage](https://developer.nulab-inc.com/docs/backlog/api/2/count-wiki-page) | Returns number of Wiki pages. |
| [getWikiPageTagList](https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page-tag-list) | Returns list of tags that are used in the project. |
| [addWikiPage](https://developer.nulab-inc.com/docs/backlog/api/2/add-wiki-page) | Adds new Wiki page. |
| [getWikiPage](https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page) | Returns information about Wiki page. |
| [updateWikiPage](https://developer.nulab-inc.com/docs/backlog/api/2/update-wiki-page) | Updates information about Wiki page. |
| [deleteWikiPage](https://developer.nulab-inc.com/docs/backlog/api/2/delete-wiki-page) | Deletes Wiki page. |
| [getListOfWikiAttachments](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-wiki-attachments) | Gets list of files attached to Wiki. |
| [attachFileToWiki](https://developer.nulab-inc.com/docs/backlog/api/2/attach-file-to-wiki) | Attaches file to Wiki |
| [getWikiPageAttachment](https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page-attachment) | Downloads Wiki page’s attachment file. |
| [removeWikiAttachment](https://developer.nulab-inc.com/docs/backlog/api/2/remove-wiki-attachment) | Removes files attached to Wiki. |
| [getListOfSharedFilesOnWiki](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-shared-files-on-wiki) | Returns the list of Shared Files on Wiki. |
| [linkSharedFilesToWiki](https://developer.nulab-inc.com/docs/backlog/api/2/link-shared-files-to-wiki) | Links Shared Files to Wiki. |
| [removeLinkToSharedFileFromWiki](https://developer.nulab-inc.com/docs/backlog/api/2/remove-link-to-shared-file-from-wiki) | Removes link to shared file from Wiki. |
| [getWikiPageHistory](https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page-history) | Returns history of Wiki page. |
| [getWikiPageStar](https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page-star) | Returns list of stars received on the Wiki page. |
| [addStar](https://developer.nulab-inc.com/docs/backlog/api/2/add-star) | Adds star. |
| [getNotification](https://developer.nulab-inc.com/docs/backlog/api/2/get-notification) | Returns own notifications. |
| [countNotification](https://developer.nulab-inc.com/docs/backlog/api/2/count-notification) | Returns number of Notifications. |
| [resetUnreadNotificationCount](https://developer.nulab-inc.com/docs/backlog/api/2/reset-unread-notification-count) | Resets unread Notification count. |
| [readNotification](https://developer.nulab-inc.com/docs/backlog/api/2/read-notification) | Changes notifications read. |
| [getListOfGitRepositories](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-git-repositories) | Returns list of Git repositories. |
| [getGitRepository](https://developer.nulab-inc.com/docs/backlog/api/2/get-git-repository) | Returns Git repository. |
| [getPullRequestList](https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request-list) | Returns list of pull requests. |
| [getNumberOfPullRequests](https://developer.nulab-inc.com/docs/backlog/api/2/get-number-of-pull-requests) | Returns number of pull requests. |
| [addPullRequest](https://developer.nulab-inc.com/docs/backlog/api/2/add-pull-request) | Adds pull requests. |
| [getPullRequest](https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request) | Returns pull reuqest. |
| [updatePullRequest](https://developer.nulab-inc.com/docs/backlog/api/2/update-pull-request) | Updates pull requests. |
| [getPullRequestComment](https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request-comment) | Returns list of pull request comments. |
| [addPullRequestComment](https://developer.nulab-inc.com/docs/backlog/api/2/add-pull-request-comment) | Adds comments on pull requests. |
| [getNumberOfPullRequestComments](https://developer.nulab-inc.com/docs/backlog/api/2/get-number-of-pull-request-comments) | Returns number of comments on pull requests. |
| [updatePullRequestCommentInformation](https://developer.nulab-inc.com/docs/backlog/api/2/update-pull-request-comment-information) | Updates pull request comment information.Authenticated user can update his own comments. |
| [getListOfPullRequestAttachment](https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-pull-request-attachment) | Returns list of attached files on pull requests. |
| [downloadPullRequestAttachment](https://developer.nulab-inc.com/docs/backlog/api/2/download-pull-request-attachment) | Downloads attached files on pull requests. |
| [deletePullRequestAttachments](https://developer.nulab-inc.com/docs/backlog/api/2/delete-pull-request-attachments) | Deletes attached files on pull requests. |
| [getWatchingList](https://developer.nulab-inc.com/docs/backlog/api/2/get-watching-list) | Returns list of your watching issues. |
| [countWatching](https://developer.nulab-inc.com/docs/backlog/api/2/count-watching) | Returns the number of your watching issues. |
| [getWatching](https://developer.nulab-inc.com/docs/backlog/api/2/get-watching) | Returns the information about a watching. |
| [addWatching](https://developer.nulab-inc.com/docs/backlog/api/2/add-watching) | Adds a watching. User can add a own watching. |
| [updateWatching](https://developer.nulab-inc.com/docs/backlog/api/2/update-watching) | Updates a watching. User can update own note. |
| [deleteWatching](https://developer.nulab-inc.com/docs/backlog/api/2/delete-watching) | Deletes a own watching.User can delete a own watching. |
| [markWatchingAsRead](https://developer.nulab-inc.com/docs/backlog/api/2/mark-watching-as-read) | Mark a watching as read. |
| [getProjectGroupList](https://developer.nulab-inc.com/docs/backlog/api/2/get-project-group-list) | Returns list of project groups. |
| [addProjectGroup](https://developer.nulab-inc.com/docs/backlog/api/2/add-project-group) | Add group to project. |
| [deleteProjectGroup](https://developer.nulab-inc.com/docs/backlog/api/2/delete-project-group) | Removes a group from the project. |
| [getGroupIcon](https://developer.nulab-inc.com/docs/backlog/api/2/get-group-icon) | Downloads group icon. |
| [getLicence](https://developer.nulab-inc.com/docs/backlog/api/2/get-licence) | Returns licence. |
