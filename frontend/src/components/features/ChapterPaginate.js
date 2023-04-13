import React from "react";
import { Pagination } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";

const ChapterPaginate = ({ pages, page, isAdmin = false, keyword = "" }) => {
  if (keyword) {
    keyword = keyword.split("?keyword=")[1].split("&")[0];
  }
  return (
    pages > 1 && (
      <Pagination>
        {[...Array(pages).keys()].map((x) => (
          <LinkContainer
            key={x + 1}
            to={
              !isAdmin
                ? `/blog/?keyword=${keyword}&page=${x + 1}`
                : `/admin/chapterslist/?keyword=${keyword}&page=${x + 1}`
            }
          >
            <Pagination.Item active={x + 1 === page}>{x + 1}</Pagination.Item>
          </LinkContainer>
        ))}
      </Pagination>
    )
  );
};

export default ChapterPaginate;
