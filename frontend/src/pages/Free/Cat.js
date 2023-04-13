import React, { Fragment, useEffect } from "react";
import { listcategorysDetails } from "../../actions/categoryActions";
import { useDispatch, useSelector } from "react-redux";
import Loader from "../../components/features/Loader";
import Message from "../../components/features/Message";
import { Container, Row, Col } from "react-bootstrap";
import ComicItems from "../../components/features/ComicItems";

const Cat = ({ match }) => {
  const catId = match.params.id;
  const dispatch = useDispatch();
  const { comics, error, loading, category } = useSelector(
    (state) => state.categoryDetails
  );
  useEffect(() => {
    dispatch(listcategorysDetails(catId));
  }, [dispatch, catId]);
  return (
    <Fragment>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Container>
          <Row>
            <Col>
              <h2>List Of {category?.name} Comics</h2>
            </Col>
          </Row>
          <Row>
            {comics?.map((comic) => (
              <Col sm={12} md={6} lg={4} xl={3} key={comic._id}>
                <ComicItems comic={comic} />
              </Col>
            ))}
          </Row>
        </Container>
      )}
    </Fragment>
  );
};

export default Cat;
