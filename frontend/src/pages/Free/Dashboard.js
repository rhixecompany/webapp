import React, { Fragment, useEffect } from "react";
import ComicCarousel from "../../components/features/ComicCarousel";
import ComicItems from "../../components/features/ComicItems";
import { useDispatch, useSelector } from "react-redux";
import { listComics } from "../../actions/comicsActions";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";
import Paginate from "../../components/features/Paginate";
import { Col, Row, Container } from "react-bootstrap";
const Dashboard = ({ history }) => {
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
        <div>{!keyword && <ComicCarousel />}</div>
        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant="danger">{error}</Message>
        ) : (
          <Row>
            {comics?.map((comic) => (
              <Col sm={6} md={6} lg={4} xl={3} key={comic._id}>
                <ComicItems comic={comic} />
              </Col>
            ))}
            <Paginate pages={pages} page={page} keyword={keyword} />
          </Row>
        )}
      </Container>
    </Fragment>
  );
};

export default Dashboard;
