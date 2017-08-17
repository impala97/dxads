--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.7
-- Dumped by pg_dump version 9.5.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: dxads_sch; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA dxads_sch;


ALTER SCHEMA dxads_sch OWNER TO postgres;
ALTER SCHEMA dxads_sch OWNER TO srmehta;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: citext; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;


--
-- Name: EXTENSION citext; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION citext IS 'data type for case-insensitive character strings';


SET search_path = public, pg_catalog;

--
-- Name: email; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN email AS citext
	CONSTRAINT email_check CHECK ((VALUE ~ '^[a-zA-Z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'::citext));


ALTER DOMAIN email OWNER TO postgres;
ALTER DOMAIN email OWNER TO srmehta;

SET search_path = dxads_sch, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: contact; Type: TABLE; Schema: dxads_sch; Owner: postgres
--

CREATE TABLE contact (
    id integer NOT NULL,
    name text NOT NULL,
    email public.email NOT NULL,
    message text
);


ALTER TABLE contact OWNER TO postgres;

--
-- Name: contact_id_seq; Type: SEQUENCE; Schema: dxads_sch; Owner: postgres
--

CREATE SEQUENCE contact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE contact_id_seq OWNER TO postgres;

--
-- Name: contact_id_seq; Type: SEQUENCE OWNED BY; Schema: dxads_sch; Owner: postgres
--

ALTER SEQUENCE contact_id_seq OWNED BY contact.id;


--
-- Name: login; Type: TABLE; Schema: dxads_sch; Owner: postgres
--

CREATE TABLE login (
    id integer NOT NULL,
    name text NOT NULL,
    password text NOT NULL
);


ALTER TABLE login OWNER TO postgres;

--
-- Name: login_id_seq; Type: SEQUENCE; Schema: dxads_sch; Owner: postgres
--

CREATE SEQUENCE login_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE login_id_seq OWNER TO postgres;

--
-- Name: login_id_seq; Type: SEQUENCE OWNED BY; Schema: dxads_sch; Owner: postgres
--

ALTER SEQUENCE login_id_seq OWNED BY login.id;


--
-- Name: profile; Type: TABLE; Schema: dxads_sch; Owner: postgres
--

CREATE TABLE profile (
    id integer NOT NULL,
    fname character(10) NOT NULL,
    lname character(10) NOT NULL,
    gender boolean DEFAULT true,
    age smallint NOT NULL,
    mobile character varying(10) NOT NULL,
    email public.email NOT NULL,
    init boolean DEFAULT false,
    CONSTRAINT profile_age_check CHECK ((age >= 18)),
    CONSTRAINT profile_mobile_check CHECK (((mobile)::text ~ '^[0-9]+$'::text))
);


ALTER TABLE profile OWNER TO postgres;

--
-- Name: profile_age_seq; Type: SEQUENCE; Schema: dxads_sch; Owner: postgres
--

CREATE SEQUENCE profile_age_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE profile_age_seq OWNER TO postgres;

--
-- Name: profile_age_seq; Type: SEQUENCE OWNED BY; Schema: dxads_sch; Owner: postgres
--

ALTER SEQUENCE profile_age_seq OWNED BY profile.age;


--
-- Name: profile_id_seq; Type: SEQUENCE; Schema: dxads_sch; Owner: postgres
--

CREATE SEQUENCE profile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE profile_id_seq OWNER TO postgres;

--
-- Name: profile_id_seq; Type: SEQUENCE OWNED BY; Schema: dxads_sch; Owner: postgres
--

ALTER SEQUENCE profile_id_seq OWNED BY profile.id;


--
-- Name: id; Type: DEFAULT; Schema: dxads_sch; Owner: postgres
--

ALTER TABLE ONLY contact ALTER COLUMN id SET DEFAULT nextval('contact_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: dxads_sch; Owner: postgres
--

ALTER TABLE ONLY login ALTER COLUMN id SET DEFAULT nextval('login_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: dxads_sch; Owner: postgres
--

ALTER TABLE ONLY profile ALTER COLUMN id SET DEFAULT nextval('profile_id_seq'::regclass);


--
-- Name: age; Type: DEFAULT; Schema: dxads_sch; Owner: postgres
--

ALTER TABLE ONLY profile ALTER COLUMN age SET DEFAULT nextval('profile_age_seq'::regclass);


--
-- Data for Name: contact; Type: TABLE DATA; Schema: dxads_sch; Owner: postgres
--

COPY contact (id, name, email, message) FROM stdin;
7	smit	sr_mehta@itmusketeers.com	Hello! Data successfully eneterd in database!
8	smit	sr_mehta@itmusketeers.com	Hello! data is successfully entered in database...
9	smit	sr_mehta@itmusketeers.com	test 110820171503
10	smit	sr_mehta@itmusketeers.com	test 110820171845
11	smit	sr_mehta@itmusketeers.com	test 110820171845
12	smit	sr_mehta@itmusketeers.com	test 110820171845
13	smit	sr_mehta@itmusketeers.com	test 110820171847
14	smit	sr_mehta@itmusketeers.com	test 110820171848
15	smit	sr_mehta@itmusketeers.com	test 110820171851
16	smit	sr_mehta@itmusketeers.com	test 110820171853
17	smit	sr_mehta@itmusketeers.com	test 110820171854
18	smit	sr_mehta@itmusketeers.com	
19	smit	sr_mehta@itmusketeers.com	fdf
\.


--
-- Name: contact_id_seq; Type: SEQUENCE SET; Schema: dxads_sch; Owner: postgres
--

SELECT pg_catalog.setval('contact_id_seq', 19, true);


--
-- Data for Name: login; Type: TABLE DATA; Schema: dxads_sch; Owner: postgres
--

COPY login (id, name, password) FROM stdin;
1	smit	sr@itmcs
\.


--
-- Name: login_id_seq; Type: SEQUENCE SET; Schema: dxads_sch; Owner: postgres
--

SELECT pg_catalog.setval('login_id_seq', 1, true);


--
-- Data for Name: profile; Type: TABLE DATA; Schema: dxads_sch; Owner: postgres
--

COPY profile (id, fname, lname, gender, age, mobile, email, init) FROM stdin;
1	Smit      	Mehta     	t	20	9904274495	sr_mehta@itmuskeeters.com	t
\.


--
-- Name: profile_age_seq; Type: SEQUENCE SET; Schema: dxads_sch; Owner: postgres
--

SELECT pg_catalog.setval('profile_age_seq', 1, false);


--
-- Name: profile_id_seq; Type: SEQUENCE SET; Schema: dxads_sch; Owner: postgres
--

SELECT pg_catalog.setval('profile_id_seq', 1, false);


--
-- Name: contact_pkey; Type: CONSTRAINT; Schema: dxads_sch; Owner: postgres
--

ALTER TABLE ONLY contact
    ADD CONSTRAINT contact_pkey PRIMARY KEY (id);


--
-- Name: login_name_key; Type: CONSTRAINT; Schema: dxads_sch; Owner: postgres
--

ALTER TABLE ONLY login
    ADD CONSTRAINT login_name_key UNIQUE (name);


--
-- Name: login_pkey; Type: CONSTRAINT; Schema: dxads_sch; Owner: postgres
--

ALTER TABLE ONLY login
    ADD CONSTRAINT login_pkey PRIMARY KEY (id);


--
-- Name: profile_pkey; Type: CONSTRAINT; Schema: dxads_sch; Owner: postgres
--

ALTER TABLE ONLY profile
    ADD CONSTRAINT profile_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO srmehta;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

