--
-- PostgreSQL database dump
--

\restrict DqKahhlWy4Uwkx4a7p3X3PU4pP7D9QlEv07xYM50siHJJTgrp7SJXFlbRIIsUV5

-- Dumped from database version 17.5 (Postgres.app)
-- Dumped by pg_dump version 17.6 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    username character varying(60) NOT NULL
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    "Telegram ID" bigint NOT NULL,
    "Username" character varying(33) NOT NULL,
    "Телефон" character varying(16),
    "Дата первого захода" timestamp without time zone NOT NULL,
    "UTM-метки" character varying(50),
    "Промокод отправленный" character varying(9),
    "Дата отправки промокода" timestamp without time zone,
    "Размер скидки обещанный" character varying(4)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (username) FROM stdin;
Aridkruchinin
fgfd
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, "Telegram ID", "Username", "Телефон", "Дата первого захода", "UTM-метки", "Промокод отправленный", "Дата отправки промокода", "Размер скидки обещанный") FROM stdin;
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 21, true);


--
-- Name: users users_Telegram ID_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT "users_Telegram ID_key" UNIQUE ("Telegram ID");


--
-- Name: users users_Username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT "users_Username_key" UNIQUE ("Username");


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_Промокод отправленный_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT "users_Промокод отправленный_key" UNIQUE ("Промокод отправленный");


--
-- Name: users users_Телефон_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT "users_Телефон_key" UNIQUE ("Телефон");


--
-- PostgreSQL database dump complete
--

\unrestrict DqKahhlWy4Uwkx4a7p3X3PU4pP7D9QlEv07xYM50siHJJTgrp7SJXFlbRIIsUV5

