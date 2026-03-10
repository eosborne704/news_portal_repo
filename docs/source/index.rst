.. News_Portal documentation master file, created by
   sphinx-quickstart on Wed Mar  4 16:21:11 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

News_Portal documentation
=========================


Project Overview
----------------

News_Portal is a Django-based web application that allows users to register as readers, editors, or journalists.

- **Readers** can access approved articles and subscribe to newsletters from publishers and journalists. They receive updates and can comment on articles.
- **Journalists** can write articles and newsletters. Their content is sent via email and, upon editor approval, is published to the news page. Journalists can also manage their own newsletters.
- **Editors** review, edit, and approve articles and newsletters for release. Editors ensure content quality and manage publication workflows.

Additional Features:
- Secure password reset functionality for all users.
- RESTful API integration for programmatic access to articles, newsletters, and user management.
- Role-based access control and permissions.
- Smooth workflow for article approval and newsletter publication.

For more details, see the generated documentation below.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
      models
      api
      usage

