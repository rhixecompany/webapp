import React, { useEffect, Fragment } from "react";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";
import { useDispatch, useSelector } from "react-redux";
import { listComics } from "../../actions/comicsActions";

import { Col, Row, Container } from "react-bootstrap";
import Paginate from "../../components/features/Paginate";

import Comics from "../../components/features/Comics";
import ComicCarousel from "../../components/features/ComicCarousel";
const Home = ({ history }) => {
  let keyword = history.location.search;

  const dispatch = useDispatch();
  const comicsList = useSelector((state) => state.comicsList);
  const { comics, error, loading, pages, page } = comicsList;

  useEffect(() => {
    dispatch(listComics(keyword));
  }, [dispatch, keyword]);
  return (
    <Fragment>
      <Container>
        {!keyword && <ComicCarousel />}

        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant="danger">{error}</Message>
        ) : (
          <Row className="Boxcontainer">
            {comics?.map((comic) => (
              <Col sm={12} md={6} lg={4} xl={3} key={comic._id}>
                <Comics comic={comic} />
              </Col>
            ))}
            <Paginate pages={pages} page={page} keyword={keyword} />
          </Row>
        )}
      </Container>
    </Fragment>
  );
};

export default Home;
