# Vue Dashboard 
The front-end of the application consists of a Vue dashboard, presenting the data to authenticated users. It is built in the same _provider agnostic_ way as the other parts of the application, allowing you to swap out different tools for authentication and database integration.

## Parts of the dashboard
The app consists of two parts: a home page which presents the posts with misinformation and some numbers. The other page is the labeling page, where authenticated users can label the retrieved posts. N.B.: only labeled posts will appear in the dashboard. The human in the loop is important here.
