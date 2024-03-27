--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: courses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.courses (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    duration interval,
    paid boolean NOT NULL
);


ALTER TABLE public.courses OWNER TO postgres;

--
-- Name: courses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.courses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.courses_id_seq OWNER TO postgres;

--
-- Name: courses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.courses_id_seq OWNED BY public.courses.id;


--
-- Name: enrollments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollments (
    id integer NOT NULL,
    student_id integer NOT NULL,
    course_id integer NOT NULL,
    enrollment_time timestamp without time zone NOT NULL
);


ALTER TABLE public.enrollments OWNER TO postgres;

--
-- Name: enrollments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollments_id_seq OWNER TO postgres;

--
-- Name: enrollments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollments_id_seq OWNED BY public.enrollments.id;


--
-- Name: students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    first_name character varying(100),
    last_name character varying(100) NOT NULL,
    email character varying(50) NOT NULL
);


ALTER TABLE public.students OWNER TO postgres;

--
-- Name: students_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.students_id_seq OWNER TO postgres;

--
-- Name: students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.students_id_seq OWNED BY public.students.id;


--
-- Name: courses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses ALTER COLUMN id SET DEFAULT nextval('public.courses_id_seq'::regclass);


--
-- Name: enrollments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollments ALTER COLUMN id SET DEFAULT nextval('public.enrollments_id_seq'::regclass);


--
-- Name: students id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students ALTER COLUMN id SET DEFAULT nextval('public.students_id_seq'::regclass);


--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.courses (id, title, duration, paid) FROM stdin;
1	Algorithms and Data Structures	10 days	f
2	Learning Data Structure and Algorithms in Python from Scratch	14 days	f
3	Object Oriented Programming in Java	7 days	f
4	IBM Full Stack Software Developer	3 mons	t
5	Introduction to Front-End Development	\N	f
6	HTML, CSS, and Javascript for Web Developers	5 days	f
7	Front End Web Development	14 days	t
8	SQL for Data Science	5 days	f
9	PostgreSQL for Everybody 	5 days	f
10	SQLite Databases | Python Programming	\N	f
11	NoSQL Databases	7 days	f
12	Introduction to MongoDB	21 days	t
13	Introduction to Data Science in Python	2 mons	f
14	Applied Machine Learning in Python	2 mons	t
15	Deep Learning	3 mons	t
16	Convolutional Neural Networks	20 days	t
\.


--
-- Data for Name: enrollments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollments (id, student_id, course_id, enrollment_time) FROM stdin;
1	22	11	2024-02-15 15:23:10
2	18	5	2024-03-20 18:30:00
3	5	5	2023-10-20 21:11:41
4	19	4	2024-01-02 07:10:54
5	6	13	2024-03-01 00:01:00
6	18	16	2023-08-29 11:37:24
7	14	2	2024-03-26 02:04:37
8	17	5	2024-02-02 02:30:00
9	14	5	2024-02-05 07:59:50
10	14	11	2024-02-11 20:00:00
11	6	9	2022-06-25 15:55:00
12	17	16	2023-10-20 21:11:00
13	1	16	2024-03-25 09:54:00
14	11	15	2024-01-01 23:00:03
15	7	12	2024-01-31 11:30:00
16	2	14	2023-06-01 12:08:25
17	13	11	2024-02-29 12:08:01
18	24	14	2024-03-20 20:09:07
19	12	4	2023-11-30 17:45:00
20	2	9	2024-02-07 07:41:21
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.students (id, username, first_name, last_name, email) FROM stdin;
1	blah91antony	Tony	Baldwin	t.baldwin@gmail.com
2	tomato_dos71	Lisa	Dickinson	lisa71dos@gmail.com
3	me8_represent	Dean	Underwood	dean.underwood97@yahoo.com
4	ewindustrialize	Elise	Romero	elise11romero@gmail.com
5	sam00potato	Samuel	Chavez	s.chavez@icloud.com
6	emily007	Emiliana	Melton	melton.em10@gmail.com
7	lisa744	Lisa	Carpenter	l.carpenter77@gmail.com
8	fictional_carl	Pat	Carlson	carlson856@outlook.com
9	boxinggoalboots	Martin	Stanton	martin56s@gmail.com
10	i_love_badminton	Alex	Underwood	al989@proton.me
11	phillipswriting	Max	Phillips	max51phillips@gmail.com
12	colonization_way	\N	Raymond	j.raymond95@yahoo.com
13	cyber_space84	Gregory	McLean	g.maclean@gmail.com
14	BreezeWriting	Sebastian	Santiago	s05santiago@gmail.com
15	TropicalTornado	Martin	Beaulieu	bb65mar@proton.me
16	darkGrayff	Jennifer	Stone	stone.j@outlook.com
17	jurassic_park_2	Lillian	Sauveterre	lilly485@outlook.com
18	freshlemon986	Lillian	Raymond	lillian.raymond001@gmail.com
19	bond007_clark	James	Clark	j.clark8855@gmail.com
20	book_queen02	Holly	Carter	holly.carter0605@outlook.com
21	CannyAnnie	Annie	White	annie.white@icloud.com
22	directorpennington	Stephanie	Pennington	s.pennington0707@gmail.com
23	ngc1569starwars	Steven	Weber	weber61615@gmail.com
24	everGreenAlb	Albert	Richardson	rich54.alb@proton.me
\.


--
-- Name: courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.courses_id_seq', 16, true);


--
-- Name: enrollments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollments_id_seq', 20, true);


--
-- Name: students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.students_id_seq', 24, true);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- Name: enrollments enrollments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_pkey PRIMARY KEY (id);


--
-- Name: enrollments enrollments_student_id_course_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_student_id_course_id_key UNIQUE (student_id, course_id);


--
-- Name: students students_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_email_key UNIQUE (email);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (id);


--
-- Name: students students_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_username_key UNIQUE (username);


--
-- Name: enrollments enrollments_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id);


--
-- Name: enrollments enrollments_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id);


--
-- PostgreSQL database dump complete
--

