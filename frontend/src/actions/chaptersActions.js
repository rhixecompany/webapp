import axios from "axios";
import {
  CHAPTERS_LIST_REQUEST,
  CHAPTERS_LIST_SUCCESS,
  CHAPTERS_LIST_FAIL,
  CHAPTERS_DETAILS_REQUEST,
  CHAPTERS_DETAILS_SUCCESS,
  CHAPTERS_DETAILS_FAIL,
  CHAPTERS_DELETE_REQUEST,
  CHAPTERS_DELETE_SUCCESS,
  CHAPTERS_DELETE_FAIL,
  CHAPTERS_CREATE_REQUEST,
  CHAPTERS_CREATE_SUCCESS,
  CHAPTERS_CREATE_FAIL,
  CHAPTERS_UPDATE_REQUEST,
  CHAPTERS_UPDATE_SUCCESS,
  CHAPTERS_UPDATE_FAIL,
  CHAPTER_CREATE_REVIEW_REQUEST,
  CHAPTER_CREATE_REVIEW_SUCCESS,
  CHAPTER_CREATE_REVIEW_FAIL,
} from "../constants/chaptersConstants";
import { logout } from "./userActions";

export const listChapters =
  (keyword = "") =>
  async (dispatch, getState) => {
    try {
      dispatch({ type: CHAPTERS_LIST_REQUEST });
      const {
        userLogin: { userInfo },
      } = getState();

      const config = {
        headers: {
          "Content-type": "application/json",
          Authorization: `Bearer ${userInfo.token}`,
        },
      };
      const { data } = await axios.get(`/api/chapters/${keyword}`, config);
      // const { data } = await axios.get(`/api/chapters/`);

      dispatch({
        type: CHAPTERS_LIST_SUCCESS,
        payload: data,
      });
    } catch (error) {
      const message =
        error.response && error.response.data.message
          ? error.response.data.message
          : error.message;
      if (message === "Not authorized, token failed") {
        dispatch(logout());
      }
      dispatch({
        type: CHAPTERS_LIST_FAIL,
        payload:
          error.response && error.response.data.detail
            ? error.response.data.detail
            : error.message,
      });
    }
  };

export const listChapterDetails = (name) => async (dispatch, getState) => {
  try {
    dispatch({ type: CHAPTERS_DETAILS_REQUEST });
    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${userInfo.token}`,
      },
    };

    const { data } = await axios.get(`/api/chapters/${name}/`, config);

    dispatch({
      type: CHAPTERS_DETAILS_SUCCESS,
      payload: data,
    });
  } catch (error) {
    const message =
      error.response && error.response.data.message
        ? error.response.data.message
        : error.message;
    if (message === "Unauthorized") {
      dispatch(logout());
    }
    dispatch({
      type: CHAPTERS_DETAILS_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const deleteChapter = (id) => async (dispatch, getState) => {
  try {
    dispatch({
      type: CHAPTERS_DELETE_REQUEST,
    });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${userInfo.token}`,
      },
    };

    const { data } = await axios.delete(`/api/chapters/delete/${id}/`, config);
    console.log(data);
    dispatch({
      type: CHAPTERS_DELETE_SUCCESS,
    });
  } catch (error) {
    dispatch({
      type: CHAPTERS_DELETE_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const createChapter = () => async (dispatch, getState) => {
  try {
    dispatch({
      type: CHAPTERS_CREATE_REQUEST,
    });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${userInfo.token}`,
      },
    };

    const { data } = await axios.post(`/api/chapters/create/`, {}, config);
    dispatch({
      type: CHAPTERS_CREATE_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: CHAPTERS_CREATE_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const updateChapter = (chapter) => async (dispatch, getState) => {
  try {
    dispatch({
      type: CHAPTERS_UPDATE_REQUEST,
    });

    const {
      userLogin: { userInfo },
    } = getState();

    const config = {
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${userInfo.token}`,
      },
    };

    const { data } = await axios.put(
      `/api/chapters/update/${chapter.id}/`,
      chapter,
      config
    );
    dispatch({
      type: CHAPTERS_UPDATE_SUCCESS,
      payload: data,
    });

    dispatch({
      type: CHAPTERS_DETAILS_SUCCESS,
      payload: data,
    });
  } catch (error) {
    dispatch({
      type: CHAPTERS_UPDATE_FAIL,
      payload:
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message,
    });
  }
};

export const createChapterReview =
  (chapterId, review) => async (dispatch, getState) => {
    try {
      dispatch({
        type: CHAPTER_CREATE_REVIEW_REQUEST,
      });

      const {
        userLogin: { userInfo },
      } = getState();

      const config = {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${userInfo.token}`,
        },
      };

      await axios.post(`/api/chapters/${chapterId}/reviews/`, review, config);

      dispatch({
        type: CHAPTER_CREATE_REVIEW_SUCCESS,
      });
    } catch (error) {
      const message =
        error.response && error.response.data.message
          ? error.response.data.message
          : error.message;
      if (message === "Not authorized, token failed") {
        dispatch(logout());
      }
      dispatch({
        type: CHAPTER_CREATE_REVIEW_FAIL,
        payload: message,
      });
    }
  };
