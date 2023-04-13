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
  CHAPTERS_CREATE_RESET,
  CHAPTERS_UPDATE_REQUEST,
  CHAPTERS_UPDATE_SUCCESS,
  CHAPTERS_UPDATE_FAIL,
  CHAPTERS_UPDATE_RESET,
  CHAPTERS_TOP_REQUEST,
  CHAPTERS_TOP_SUCCESS,
  CHAPTERS_TOP_FAIL,
  CHAPTER_CREATE_REVIEW_FAIL,
  CHAPTER_CREATE_REVIEW_REQUEST,
  CHAPTER_CREATE_REVIEW_SUCCESS,
  CHAPTER_CREATE_REVIEW_RESET,
} from "../constants/chaptersConstants";

export const chaptersListReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTERS_LIST_REQUEST:
      return { loading: true };

    case CHAPTERS_LIST_SUCCESS:
      return {
        ...state,
        loading: false,
        chapters: action.payload.result,
        count: action.payload.count,
        pages: action.payload.pages,
        page: action.payload.page,
      };

    case CHAPTERS_LIST_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const chapterDetailsReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTERS_DETAILS_REQUEST:
      return { loading: true };

    case CHAPTERS_DETAILS_SUCCESS:
      return {
        ...state,
        loading: false,
        chapter: action.payload.chapter,
        pages: action.payload.pages,
        comic: action.payload.comic,
        chapters: action.payload.comic.chapters,
      };

    case CHAPTERS_DETAILS_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const chapterDeleteReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTERS_DELETE_REQUEST:
      return { loading: true };

    case CHAPTERS_DELETE_SUCCESS:
      return { loading: false, success: true };

    case CHAPTERS_DELETE_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const chapterCreateReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTERS_CREATE_REQUEST:
      return { loading: true };

    case CHAPTERS_CREATE_SUCCESS:
      return { loading: false, success: true, chapter: action.payload };

    case CHAPTERS_CREATE_FAIL:
      return { loading: false, error: action.payload };

    case CHAPTERS_CREATE_RESET:
      return {};

    default:
      return state;
  }
};

export const chapterUpdateReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTERS_UPDATE_REQUEST:
      return { loading: true };

    case CHAPTERS_UPDATE_SUCCESS:
      return { loading: false, success: true, chapter: action.payload };

    case CHAPTERS_UPDATE_FAIL:
      return { loading: false, error: action.payload };

    case CHAPTERS_UPDATE_RESET:
      return { chapter: {} };

    default:
      return state;
  }
};

export const chaptersTopRatedReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTERS_TOP_REQUEST:
      return { loading: true };

    case CHAPTERS_TOP_SUCCESS:
      return { loading: false, chapters: action.payload };

    case CHAPTERS_TOP_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
};

export const chapterReviewCreateReducer = (state = {}, action) => {
  switch (action.type) {
    case CHAPTER_CREATE_REVIEW_REQUEST:
      return { loading: true };
    case CHAPTER_CREATE_REVIEW_SUCCESS:
      return { loading: false, success: true };
    case CHAPTER_CREATE_REVIEW_FAIL:
      return { loading: false, error: action.payload };
    case CHAPTER_CREATE_REVIEW_RESET:
      return {};
    default:
      return state;
  }
};
