import React from "react";
import PageTemplate from "../components/PageTemplate";

const NotFoundPage: React.FC = () => {
  return (
    <PageTemplate title="Page Not Found">
      <p>The page you're looking for doesn't exist.</p>
    </PageTemplate>
  );
};

export default NotFoundPage;
