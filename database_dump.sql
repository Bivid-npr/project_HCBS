--
-- PostgreSQL database dump
--

\restrict xI1PDhbXKeaV2jTudnI5nZgqtTiuva5UmQZB6EOfBc8FXkUAC9bpOOx32EyR17y

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

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

DROP DATABASE IF EXISTS "UWE cinema booking";
--
-- Name: UWE cinema booking; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "UWE cinema booking" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';


ALTER DATABASE "UWE cinema booking" OWNER TO postgres;

\unrestrict xI1PDhbXKeaV2jTudnI5nZgqtTiuva5UmQZB6EOfBc8FXkUAC9bpOOx32EyR17y
\encoding SQL_ASCII
\connect -reuse-previous=on "dbname='UWE cinema booking'"
\restrict xI1PDhbXKeaV2jTudnI5nZgqtTiuva5UmQZB6EOfBc8FXkUAC9bpOOx32EyR17y

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

--
-- Name: booking_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.booking_status AS ENUM (
    'CONFIRMED',
    'CANCELLED',
    'COMPLETED'
);


ALTER TYPE public.booking_status OWNER TO postgres;

--
-- Name: seat_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.seat_status AS ENUM (
    'AVAILABLE',
    'RESERVED',
    'BOOKED'
);


ALTER TYPE public.seat_status OWNER TO postgres;

--
-- Name: seat_type; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.seat_type AS ENUM (
    'LOWER_HALL',
    'UPPER_GALLERY',
    'VIP'
);


ALTER TYPE public.seat_type OWNER TO postgres;

--
-- Name: show_time; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.show_time AS ENUM (
    'MORNING',
    'AFTERNOON',
    'EVENING'
);


ALTER TYPE public.show_time OWNER TO postgres;

--
-- Name: show_time_cat; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.show_time_cat AS ENUM (
    'MORNING',
    'AFTERNOON',
    'EVENING'
);


ALTER TYPE public.show_time_cat OWNER TO postgres;

--
-- Name: user_role; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.user_role AS ENUM (
    'BOOKING_STAFF',
    'ADMIN',
    'MANAGER'
);


ALTER TYPE public.user_role OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: booking; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.booking (
    booking_id integer NOT NULL,
    booking_reference character varying(50) NOT NULL,
    customer_id integer NOT NULL,
    listing_id integer NOT NULL,
    user_id integer NOT NULL,
    booking_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total_price numeric(10,2) NOT NULL,
    status public.booking_status DEFAULT 'CONFIRMED'::public.booking_status NOT NULL
);


ALTER TABLE public.booking OWNER TO postgres;

--
-- Name: booking_booking_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.booking_booking_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.booking_booking_id_seq OWNER TO postgres;

--
-- Name: booking_booking_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.booking_booking_id_seq OWNED BY public.booking.booking_id;


--
-- Name: booking_seat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.booking_seat (
    booking_id integer NOT NULL,
    seat_id integer NOT NULL
);


ALTER TABLE public.booking_seat OWNER TO postgres;

--
-- Name: cinema; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cinema (
    cinema_id integer NOT NULL,
    cinema_name character varying(100) NOT NULL,
    location character varying(150),
    city_id integer NOT NULL
);


ALTER TABLE public.cinema OWNER TO postgres;

--
-- Name: city; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.city (
    city_id integer NOT NULL,
    city_name character varying(100) NOT NULL
);


ALTER TABLE public.city OWNER TO postgres;

--
-- Name: customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer (
    customer_id integer NOT NULL,
    name character varying(100),
    phone character varying(20),
    email character varying(100)
);


ALTER TABLE public.customer OWNER TO postgres;

--
-- Name: film; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.film (
    film_id integer NOT NULL,
    title character varying(150) NOT NULL,
    description text,
    genre character varying(100),
    age_rating character varying(10),
    imdb_rating numeric(3,1),
    duration integer,
    cast_members text,
    release_year integer
);


ALTER TABLE public.film OWNER TO postgres;

--
-- Name: listing; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.listing (
    listing_id integer NOT NULL,
    film_id integer NOT NULL,
    screen_id integer NOT NULL,
    show_date date NOT NULL,
    show_time time without time zone NOT NULL,
    show_time_category public.show_time_cat NOT NULL
);


ALTER TABLE public.listing OWNER TO postgres;

--
-- Name: screen; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.screen (
    screen_id integer NOT NULL,
    cinema_id integer NOT NULL,
    screen_number integer NOT NULL,
    capacity integer NOT NULL,
    CONSTRAINT screen_capacity_check CHECK (((capacity >= 50) AND (capacity <= 120)))
);


ALTER TABLE public.screen OWNER TO postgres;

--
-- Name: seat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seat (
    seat_id integer NOT NULL,
    screen_id integer NOT NULL,
    seat_number character varying(10) NOT NULL,
    seat_type public.seat_type NOT NULL,
    status public.seat_status DEFAULT 'AVAILABLE'::public.seat_status NOT NULL
);


ALTER TABLE public.seat OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(100) NOT NULL,
    password_hash text NOT NULL,
    full_name character varying(150),
    email character varying(100),
    role public.user_role NOT NULL,
    assigned_cinema_id integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: booking_details; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.booking_details AS
 SELECT b.booking_reference,
    c.name AS customer_name,
    c.phone AS customer_phone,
    c.email AS customer_email,
    f.title AS film_title,
    l.show_date,
    l.show_time,
    l.show_time_category,
    sc.screen_number,
    ci.cinema_name,
    ct.city_name,
    b.total_price,
    b.booking_date,
    b.status,
    u.full_name AS booked_by,
    count(bs.seat_id) AS ticket_count,
    string_agg((s.seat_number)::text, ', '::text ORDER BY (s.seat_number)::text) AS seat_numbers
   FROM (((((((((public.booking b
     JOIN public.customer c ON ((b.customer_id = c.customer_id)))
     JOIN public.listing l ON ((b.listing_id = l.listing_id)))
     JOIN public.film f ON ((l.film_id = f.film_id)))
     JOIN public.screen sc ON ((l.screen_id = sc.screen_id)))
     JOIN public.cinema ci ON ((sc.cinema_id = ci.cinema_id)))
     JOIN public.city ct ON ((ci.city_id = ct.city_id)))
     JOIN public.users u ON ((b.user_id = u.user_id)))
     JOIN public.booking_seat bs ON ((b.booking_id = bs.booking_id)))
     JOIN public.seat s ON ((bs.seat_id = s.seat_id)))
  GROUP BY b.booking_reference, c.name, c.phone, c.email, f.title, l.show_date, l.show_time, l.show_time_category, sc.screen_number, ci.cinema_name, ct.city_name, b.total_price, b.booking_date, b.status, u.full_name;


ALTER VIEW public.booking_details OWNER TO postgres;

--
-- Name: cinema_cinema_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cinema_cinema_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cinema_cinema_id_seq OWNER TO postgres;

--
-- Name: cinema_cinema_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cinema_cinema_id_seq OWNED BY public.cinema.cinema_id;


--
-- Name: city_city_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.city_city_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.city_city_id_seq OWNER TO postgres;

--
-- Name: city_city_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.city_city_id_seq OWNED BY public.city.city_id;


--
-- Name: customer_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customer_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customer_customer_id_seq OWNER TO postgres;

--
-- Name: customer_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customer_customer_id_seq OWNED BY public.customer.customer_id;


--
-- Name: film_film_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.film_film_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.film_film_id_seq OWNER TO postgres;

--
-- Name: film_film_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.film_film_id_seq OWNED BY public.film.film_id;


--
-- Name: listing_availability; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.listing_availability AS
 SELECT l.listing_id,
    f.title AS film_title,
    l.show_date,
    l.show_time,
    l.show_time_category,
    sc.screen_number,
    ci.cinema_name,
    st.seat_type,
    count(s.seat_id) AS available_seats
   FROM (((((public.listing l
     JOIN public.film f ON ((l.film_id = f.film_id)))
     JOIN public.screen sc ON ((l.screen_id = sc.screen_id)))
     JOIN public.cinema ci ON ((sc.cinema_id = ci.cinema_id)))
     JOIN public.seat s ON ((sc.screen_id = s.screen_id)))
     JOIN ( SELECT unnest(enum_range(NULL::public.seat_type)) AS seat_type) st ON ((s.seat_type = st.seat_type)))
  WHERE (s.status = 'AVAILABLE'::public.seat_status)
  GROUP BY l.listing_id, f.title, l.show_date, l.show_time, l.show_time_category, sc.screen_number, ci.cinema_name, st.seat_type;


ALTER VIEW public.listing_availability OWNER TO postgres;

--
-- Name: listing_listing_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.listing_listing_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.listing_listing_id_seq OWNER TO postgres;

--
-- Name: listing_listing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.listing_listing_id_seq OWNED BY public.listing.listing_id;


--
-- Name: pricing_policy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pricing_policy (
    policy_id integer NOT NULL,
    city_id integer NOT NULL,
    morning_price numeric(8,2) NOT NULL,
    afternoon_price numeric(8,2) NOT NULL,
    evening_price numeric(8,2) NOT NULL,
    upper_gallery_multiplier numeric(4,2) DEFAULT 1.20 NOT NULL,
    vip_multiplier numeric(4,2) DEFAULT 1.20 NOT NULL
);


ALTER TABLE public.pricing_policy OWNER TO postgres;

--
-- Name: pricing_policy_policy_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pricing_policy_policy_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pricing_policy_policy_id_seq OWNER TO postgres;

--
-- Name: pricing_policy_policy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pricing_policy_policy_id_seq OWNED BY public.pricing_policy.policy_id;


--
-- Name: receipt; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.receipt (
    receipt_id integer NOT NULL,
    booking_id integer NOT NULL,
    issue_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.receipt OWNER TO postgres;

--
-- Name: receipt_receipt_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.receipt_receipt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.receipt_receipt_id_seq OWNER TO postgres;

--
-- Name: receipt_receipt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.receipt_receipt_id_seq OWNED BY public.receipt.receipt_id;


--
-- Name: report_bookings_per_listing; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.report_bookings_per_listing AS
 SELECT l.listing_id,
    f.title AS film_title,
    l.show_date,
    l.show_time_category,
    ci.cinema_name,
    count(b.booking_id) AS total_bookings,
    sum(b.total_price) AS total_revenue
   FROM ((((public.listing l
     JOIN public.film f ON ((l.film_id = f.film_id)))
     JOIN public.screen sc ON ((l.screen_id = sc.screen_id)))
     JOIN public.cinema ci ON ((sc.cinema_id = ci.cinema_id)))
     LEFT JOIN public.booking b ON (((l.listing_id = b.listing_id) AND (b.status <> 'CANCELLED'::public.booking_status))))
  GROUP BY l.listing_id, f.title, l.show_date, l.show_time_category, ci.cinema_name
  ORDER BY l.show_date, ci.cinema_name;


ALTER VIEW public.report_bookings_per_listing OWNER TO postgres;

--
-- Name: report_monthly_revenue; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.report_monthly_revenue AS
 SELECT ci.cinema_name,
    ct.city_name,
    EXTRACT(year FROM b.booking_date) AS year,
    EXTRACT(month FROM b.booking_date) AS month,
    count(b.booking_id) AS total_bookings,
    sum(b.total_price) AS total_revenue
   FROM ((((public.booking b
     JOIN public.listing l ON ((b.listing_id = l.listing_id)))
     JOIN public.screen sc ON ((l.screen_id = sc.screen_id)))
     JOIN public.cinema ci ON ((sc.cinema_id = ci.cinema_id)))
     JOIN public.city ct ON ((ci.city_id = ct.city_id)))
  WHERE (b.status <> 'CANCELLED'::public.booking_status)
  GROUP BY ci.cinema_name, ct.city_name, (EXTRACT(year FROM b.booking_date)), (EXTRACT(month FROM b.booking_date))
  ORDER BY (EXTRACT(year FROM b.booking_date)) DESC, (EXTRACT(month FROM b.booking_date)) DESC, (sum(b.total_price)) DESC;


ALTER VIEW public.report_monthly_revenue OWNER TO postgres;

--
-- Name: report_staff_performance; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.report_staff_performance AS
 SELECT u.full_name,
    u.username,
    EXTRACT(year FROM b.booking_date) AS year,
    EXTRACT(month FROM b.booking_date) AS month,
    count(b.booking_id) AS bookings_made,
    sum(b.total_price) AS revenue_generated
   FROM (public.booking b
     JOIN public.users u ON ((b.user_id = u.user_id)))
  WHERE ((b.status <> 'CANCELLED'::public.booking_status) AND (u.role = 'BOOKING_STAFF'::public.user_role))
  GROUP BY u.user_id, u.full_name, u.username, (EXTRACT(year FROM b.booking_date)), (EXTRACT(month FROM b.booking_date))
  ORDER BY (EXTRACT(year FROM b.booking_date)) DESC, (EXTRACT(month FROM b.booking_date)) DESC, (count(b.booking_id)) DESC;


ALTER VIEW public.report_staff_performance OWNER TO postgres;

--
-- Name: report_top_revenue_film; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.report_top_revenue_film AS
 SELECT f.title,
    f.genre,
    count(b.booking_id) AS total_bookings,
    sum(b.total_price) AS total_revenue
   FROM ((public.booking b
     JOIN public.listing l ON ((b.listing_id = l.listing_id)))
     JOIN public.film f ON ((l.film_id = f.film_id)))
  WHERE (b.status <> 'CANCELLED'::public.booking_status)
  GROUP BY f.film_id, f.title, f.genre
  ORDER BY (sum(b.total_price)) DESC;


ALTER VIEW public.report_top_revenue_film OWNER TO postgres;

--
-- Name: screen_screen_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.screen_screen_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.screen_screen_id_seq OWNER TO postgres;

--
-- Name: screen_screen_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.screen_screen_id_seq OWNED BY public.screen.screen_id;


--
-- Name: seat_seat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seat_seat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seat_seat_id_seq OWNER TO postgres;

--
-- Name: seat_seat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.seat_seat_id_seq OWNED BY public.seat.seat_id;


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: booking booking_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking ALTER COLUMN booking_id SET DEFAULT nextval('public.booking_booking_id_seq'::regclass);


--
-- Name: cinema cinema_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cinema ALTER COLUMN cinema_id SET DEFAULT nextval('public.cinema_cinema_id_seq'::regclass);


--
-- Name: city city_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.city ALTER COLUMN city_id SET DEFAULT nextval('public.city_city_id_seq'::regclass);


--
-- Name: customer customer_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer ALTER COLUMN customer_id SET DEFAULT nextval('public.customer_customer_id_seq'::regclass);


--
-- Name: film film_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.film ALTER COLUMN film_id SET DEFAULT nextval('public.film_film_id_seq'::regclass);


--
-- Name: listing listing_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listing ALTER COLUMN listing_id SET DEFAULT nextval('public.listing_listing_id_seq'::regclass);


--
-- Name: pricing_policy policy_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pricing_policy ALTER COLUMN policy_id SET DEFAULT nextval('public.pricing_policy_policy_id_seq'::regclass);


--
-- Name: receipt receipt_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.receipt ALTER COLUMN receipt_id SET DEFAULT nextval('public.receipt_receipt_id_seq'::regclass);


--
-- Name: screen screen_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.screen ALTER COLUMN screen_id SET DEFAULT nextval('public.screen_screen_id_seq'::regclass);


--
-- Name: seat seat_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seat ALTER COLUMN seat_id SET DEFAULT nextval('public.seat_seat_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: booking; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.booking (booking_id, booking_reference, customer_id, listing_id, user_id, booking_date, total_price, status) FROM stdin;
1	BK-20240001	1	1	1	2026-04-28 09:04:32.293877	12.00	CONFIRMED
2	BK-20240002	2	3	1	2026-04-29 09:04:32.293877	11.52	CONFIRMED
3	BK-20240003	3	5	2	2026-04-27 09:04:32.293877	25.20	CONFIRMED
4	BK-20240004	4	6	3	2026-04-29 09:04:32.293877	10.00	CONFIRMED
5	BK-20240005	5	2	1	2026-04-25 09:04:32.293877	14.00	CANCELLED
6	BK-7DB0589A	6	1	1	2026-05-02 08:49:07.392932	8.64	CONFIRMED
7	BK-8D88DE92	6	1	1	2026-05-02 09:02:17.822662	6.00	CONFIRMED
8	BK-1BD5DB01	7	2	7	2026-05-04 00:07:27.53838	8.40	CONFIRMED
9	BK-0303951E	8	1	7	2026-05-04 00:14:21.882281	8.64	CONFIRMED
10	BK-C0B54DD6	9	3	4	2026-05-04 20:42:49.325582	9.60	CONFIRMED
11	BK-F826FEC4	10	17	4	2026-05-04 20:54:57.866107	9.60	CONFIRMED
12	BK-A1651F1C	10	17	4	2026-05-04 20:55:44.77849	9.60	CANCELLED
\.


--
-- Data for Name: booking_seat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.booking_seat (booking_id, seat_id) FROM stdin;
1	1
1	2
2	95
3	125
3	126
3	127
6	96
7	3
8	44
9	100
10	45
11	34
12	57
\.


--
-- Data for Name: cinema; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cinema (cinema_id, cinema_name, location, city_id) FROM stdin;
1	Horizon Birmingham Central	New Street, Birmingham	1
2	Horizon Birmingham Broad St	Broad Street, Birmingham	1
3	Horizon Bristol Cabot	Cabot Circus, Bristol	2
4	Horizon Bristol Cribbs	Cribbs Causeway, Bristol	2
5	Horizon Cardiff Bay	Mermaid Quay, Cardiff	3
6	Horizon Cardiff Centre	Queen Street, Cardiff	3
7	Horizon London West End	Leicester Square, London	4
8	Horizon London East	Canary Wharf, London	4
\.


--
-- Data for Name: city; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.city (city_id, city_name) FROM stdin;
1	Birmingham
2	Bristol
3	Cardiff
4	London
\.


--
-- Data for Name: customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customer (customer_id, name, phone, email) FROM stdin;
1	Alice Johnson	07700900001	alice@email.com
2	Bob Williams	07700900002	bob@email.com
3	Carol Davis	07700900003	carol@email.com
4	David Brown	07700900004	david@email.com
5	Emma Wilson	07700900005	emma@email.com
6	ram	9749321312	girish@gmail.com
7	bkjsaD	1312312312	ASDASD@GMAIL.COM
8	dsadas	12312312	dasdas
9	fdgdsfg	213231321s	afdfs
10	dasdas	123123	adsdas
\.


--
-- Data for Name: film; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.film (film_id, title, description, genre, age_rating, imdb_rating, duration, cast_members, release_year) FROM stdin;
1	Inception	A thief who steals corporate secrets through dream-sharing technology.	Sci-Fi	PG-13	8.8	148	Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page	2010
3	Interstellar	A team of explorers travel through a wormhole in space.	Sci-Fi	PG-13	8.6	169	Matthew McConaughey, Anne Hathaway, Jessica Chastain	2014
4	Top Gun: Maverick	After thirty years, Maverick is still pushing the envelope as a top naval aviator.	Action	PG-13	8.3	130	Tom Cruise, Jennifer Connelly, Miles Teller	2022
5	Oppenheimer	The story of J. Robert Oppenheimer and the development of the atomic bomb.	Biography	R	8.3	180	Cillian Murphy, Emily Blunt, Matt Damon	2023
2	The dark knight		action	18	4.1	100		2023
6	test film	dasidasiodasd	action	12	5.0	100		2024
\.


--
-- Data for Name: listing; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.listing (listing_id, film_id, screen_id, show_date, show_time, show_time_category) FROM stdin;
2	1	1	2026-05-01	14:00:00	AFTERNOON
3	1	1	2026-05-01	19:00:00	EVENING
5	2	2	2026-05-02	15:00:00	AFTERNOON
6	3	4	2026-05-01	10:30:00	MORNING
8	4	5	2026-05-03	13:00:00	AFTERNOON
1	1	1	2026-05-01	08:00:00	MORNING
11	3	2	2026-05-03	18:00:00	MORNING
12	6	6	2026-05-03	18:00:00	MORNING
13	1	7	2026-05-03	18:00:00	MORNING
14	6	3	2026-05-03	18:00:00	MORNING
15	5	4	2026-05-04	08:00:00	MORNING
16	3	5	2026-05-04	18:00:00	EVENING
17	6	1	2026-05-06	18:00:00	EVENING
\.


--
-- Data for Name: pricing_policy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pricing_policy (policy_id, city_id, morning_price, afternoon_price, evening_price, upper_gallery_multiplier, vip_multiplier) FROM stdin;
1	1	5.00	6.00	7.00	1.20	1.20
2	2	6.00	7.00	8.00	1.20	1.20
3	3	5.00	6.00	7.00	1.20	1.20
4	4	10.00	11.00	12.00	1.20	1.20
\.


--
-- Data for Name: receipt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.receipt (receipt_id, booking_id, issue_date) FROM stdin;
1	1	2026-04-28 09:04:32.293877
2	2	2026-04-29 09:04:32.293877
3	3	2026-04-27 09:04:32.293877
4	4	2026-04-29 09:04:32.293877
5	6	2026-05-02 08:49:07.392932
6	7	2026-05-02 09:02:17.822662
7	8	2026-05-04 00:07:27.53838
8	9	2026-05-04 00:14:21.882281
9	10	2026-05-04 20:42:49.325582
10	11	2026-05-04 20:54:57.866107
11	12	2026-05-04 20:55:44.77849
\.


--
-- Data for Name: screen; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.screen (screen_id, cinema_id, screen_number, capacity) FROM stdin;
1	3	1	100
2	3	2	80
3	3	3	60
4	1	1	120
5	1	2	90
6	1	1	100
7	2	1	100
8	2	3	100
9	4	1	100
10	4	2	100
11	4	3	100
\.


--
-- Data for Name: seat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seat (seat_id, screen_id, seat_number, seat_type, status) FROM stdin;
4	1	L04	LOWER_HALL	AVAILABLE
5	1	L05	LOWER_HALL	AVAILABLE
6	1	L06	LOWER_HALL	AVAILABLE
7	1	L07	LOWER_HALL	AVAILABLE
8	1	L08	LOWER_HALL	AVAILABLE
9	1	L09	LOWER_HALL	AVAILABLE
10	1	L10	LOWER_HALL	AVAILABLE
11	1	L11	LOWER_HALL	AVAILABLE
12	1	L12	LOWER_HALL	AVAILABLE
13	1	L13	LOWER_HALL	AVAILABLE
14	1	L14	LOWER_HALL	AVAILABLE
15	1	L15	LOWER_HALL	AVAILABLE
16	1	L16	LOWER_HALL	AVAILABLE
17	1	L17	LOWER_HALL	AVAILABLE
18	1	L18	LOWER_HALL	AVAILABLE
19	1	L19	LOWER_HALL	AVAILABLE
20	1	L20	LOWER_HALL	AVAILABLE
21	1	L21	LOWER_HALL	AVAILABLE
22	1	L22	LOWER_HALL	AVAILABLE
23	1	L23	LOWER_HALL	AVAILABLE
24	1	L24	LOWER_HALL	AVAILABLE
25	1	L25	LOWER_HALL	AVAILABLE
26	1	L26	LOWER_HALL	AVAILABLE
27	1	L27	LOWER_HALL	AVAILABLE
28	1	L28	LOWER_HALL	AVAILABLE
29	1	L29	LOWER_HALL	AVAILABLE
30	1	L30	LOWER_HALL	AVAILABLE
31	1	U01	UPPER_GALLERY	AVAILABLE
32	1	U02	UPPER_GALLERY	AVAILABLE
33	1	U03	UPPER_GALLERY	AVAILABLE
35	1	U05	UPPER_GALLERY	AVAILABLE
36	1	U06	UPPER_GALLERY	AVAILABLE
37	1	U07	UPPER_GALLERY	AVAILABLE
38	1	U08	UPPER_GALLERY	AVAILABLE
39	1	U09	UPPER_GALLERY	AVAILABLE
40	1	U10	UPPER_GALLERY	AVAILABLE
41	1	U11	UPPER_GALLERY	AVAILABLE
42	1	U12	UPPER_GALLERY	AVAILABLE
43	1	U13	UPPER_GALLERY	AVAILABLE
46	1	U16	UPPER_GALLERY	AVAILABLE
47	1	U17	UPPER_GALLERY	AVAILABLE
48	1	U18	UPPER_GALLERY	AVAILABLE
49	1	U19	UPPER_GALLERY	AVAILABLE
50	1	U20	UPPER_GALLERY	AVAILABLE
51	1	U21	UPPER_GALLERY	AVAILABLE
52	1	U22	UPPER_GALLERY	AVAILABLE
53	1	U23	UPPER_GALLERY	AVAILABLE
54	1	U24	UPPER_GALLERY	AVAILABLE
55	1	U25	UPPER_GALLERY	AVAILABLE
56	1	U26	UPPER_GALLERY	AVAILABLE
58	1	U28	UPPER_GALLERY	AVAILABLE
59	1	U29	UPPER_GALLERY	AVAILABLE
60	1	U30	UPPER_GALLERY	AVAILABLE
61	1	U31	UPPER_GALLERY	AVAILABLE
62	1	U32	UPPER_GALLERY	AVAILABLE
63	1	U33	UPPER_GALLERY	AVAILABLE
64	1	U34	UPPER_GALLERY	AVAILABLE
65	1	U35	UPPER_GALLERY	AVAILABLE
66	1	U36	UPPER_GALLERY	AVAILABLE
67	1	U37	UPPER_GALLERY	AVAILABLE
68	1	U38	UPPER_GALLERY	AVAILABLE
69	1	U39	UPPER_GALLERY	AVAILABLE
70	1	U40	UPPER_GALLERY	AVAILABLE
71	1	U41	UPPER_GALLERY	AVAILABLE
72	1	U42	UPPER_GALLERY	AVAILABLE
73	1	U43	UPPER_GALLERY	AVAILABLE
74	1	U44	UPPER_GALLERY	AVAILABLE
75	1	U45	UPPER_GALLERY	AVAILABLE
76	1	U46	UPPER_GALLERY	AVAILABLE
77	1	U47	UPPER_GALLERY	AVAILABLE
78	1	U48	UPPER_GALLERY	AVAILABLE
79	1	U49	UPPER_GALLERY	AVAILABLE
80	1	U50	UPPER_GALLERY	AVAILABLE
81	1	U51	UPPER_GALLERY	AVAILABLE
82	1	U52	UPPER_GALLERY	AVAILABLE
83	1	U53	UPPER_GALLERY	AVAILABLE
84	1	U54	UPPER_GALLERY	AVAILABLE
85	1	U55	UPPER_GALLERY	AVAILABLE
86	1	U56	UPPER_GALLERY	AVAILABLE
87	1	U57	UPPER_GALLERY	AVAILABLE
88	1	U58	UPPER_GALLERY	AVAILABLE
89	1	U59	UPPER_GALLERY	AVAILABLE
90	1	U60	UPPER_GALLERY	AVAILABLE
91	1	U61	UPPER_GALLERY	AVAILABLE
92	1	U62	UPPER_GALLERY	AVAILABLE
93	1	U63	UPPER_GALLERY	AVAILABLE
94	1	U64	UPPER_GALLERY	AVAILABLE
97	1	V03	VIP	AVAILABLE
98	1	V04	VIP	AVAILABLE
99	1	V05	VIP	AVAILABLE
101	2	L01	LOWER_HALL	AVAILABLE
102	2	L02	LOWER_HALL	AVAILABLE
103	2	L03	LOWER_HALL	AVAILABLE
104	2	L04	LOWER_HALL	AVAILABLE
105	2	L05	LOWER_HALL	AVAILABLE
106	2	L06	LOWER_HALL	AVAILABLE
107	2	L07	LOWER_HALL	AVAILABLE
108	2	L08	LOWER_HALL	AVAILABLE
109	2	L09	LOWER_HALL	AVAILABLE
110	2	L10	LOWER_HALL	AVAILABLE
111	2	L11	LOWER_HALL	AVAILABLE
112	2	L12	LOWER_HALL	AVAILABLE
113	2	L13	LOWER_HALL	AVAILABLE
114	2	L14	LOWER_HALL	AVAILABLE
115	2	L15	LOWER_HALL	AVAILABLE
116	2	L16	LOWER_HALL	AVAILABLE
117	2	L17	LOWER_HALL	AVAILABLE
118	2	L18	LOWER_HALL	AVAILABLE
119	2	L19	LOWER_HALL	AVAILABLE
120	2	L20	LOWER_HALL	AVAILABLE
121	2	L21	LOWER_HALL	AVAILABLE
122	2	L22	LOWER_HALL	AVAILABLE
123	2	L23	LOWER_HALL	AVAILABLE
124	2	L24	LOWER_HALL	AVAILABLE
128	2	U04	UPPER_GALLERY	AVAILABLE
129	2	U05	UPPER_GALLERY	AVAILABLE
130	2	U06	UPPER_GALLERY	AVAILABLE
131	2	U07	UPPER_GALLERY	AVAILABLE
132	2	U08	UPPER_GALLERY	AVAILABLE
133	2	U09	UPPER_GALLERY	AVAILABLE
134	2	U10	UPPER_GALLERY	AVAILABLE
135	2	U11	UPPER_GALLERY	AVAILABLE
136	2	U12	UPPER_GALLERY	AVAILABLE
137	2	U13	UPPER_GALLERY	AVAILABLE
138	2	U14	UPPER_GALLERY	AVAILABLE
139	2	U15	UPPER_GALLERY	AVAILABLE
140	2	U16	UPPER_GALLERY	AVAILABLE
141	2	U17	UPPER_GALLERY	AVAILABLE
142	2	U18	UPPER_GALLERY	AVAILABLE
143	2	U19	UPPER_GALLERY	AVAILABLE
144	2	U20	UPPER_GALLERY	AVAILABLE
145	2	U21	UPPER_GALLERY	AVAILABLE
146	2	U22	UPPER_GALLERY	AVAILABLE
147	2	U23	UPPER_GALLERY	AVAILABLE
148	2	U24	UPPER_GALLERY	AVAILABLE
149	2	U25	UPPER_GALLERY	AVAILABLE
150	2	U26	UPPER_GALLERY	AVAILABLE
151	2	U27	UPPER_GALLERY	AVAILABLE
152	2	U28	UPPER_GALLERY	AVAILABLE
153	2	U29	UPPER_GALLERY	AVAILABLE
154	2	U30	UPPER_GALLERY	AVAILABLE
155	2	U31	UPPER_GALLERY	AVAILABLE
156	2	U32	UPPER_GALLERY	AVAILABLE
157	2	U33	UPPER_GALLERY	AVAILABLE
96	1	V02	VIP	BOOKED
3	1	L03	LOWER_HALL	BOOKED
44	1	U14	UPPER_GALLERY	BOOKED
100	1	V06	VIP	BOOKED
45	1	U15	UPPER_GALLERY	BOOKED
34	1	U04	UPPER_GALLERY	BOOKED
57	1	U27	UPPER_GALLERY	AVAILABLE
158	2	U34	UPPER_GALLERY	AVAILABLE
159	2	U35	UPPER_GALLERY	AVAILABLE
160	2	U36	UPPER_GALLERY	AVAILABLE
161	2	U37	UPPER_GALLERY	AVAILABLE
162	2	U38	UPPER_GALLERY	AVAILABLE
163	2	U39	UPPER_GALLERY	AVAILABLE
164	2	U40	UPPER_GALLERY	AVAILABLE
165	2	U41	UPPER_GALLERY	AVAILABLE
166	2	U42	UPPER_GALLERY	AVAILABLE
167	2	U43	UPPER_GALLERY	AVAILABLE
168	2	U44	UPPER_GALLERY	AVAILABLE
169	2	U45	UPPER_GALLERY	AVAILABLE
170	2	U46	UPPER_GALLERY	AVAILABLE
171	2	U47	UPPER_GALLERY	AVAILABLE
172	2	U48	UPPER_GALLERY	AVAILABLE
173	2	U49	UPPER_GALLERY	AVAILABLE
174	2	U50	UPPER_GALLERY	AVAILABLE
175	2	V01	VIP	AVAILABLE
176	2	V02	VIP	AVAILABLE
177	2	V03	VIP	AVAILABLE
178	2	V04	VIP	AVAILABLE
179	2	V05	VIP	AVAILABLE
180	2	V06	VIP	AVAILABLE
1	1	L01	LOWER_HALL	BOOKED
127	2	U03	UPPER_GALLERY	BOOKED
2	1	L02	LOWER_HALL	BOOKED
125	2	U01	UPPER_GALLERY	BOOKED
126	2	U02	UPPER_GALLERY	BOOKED
95	1	V01	VIP	BOOKED
181	6	L01	LOWER_HALL	AVAILABLE
182	6	L02	LOWER_HALL	AVAILABLE
183	6	L03	LOWER_HALL	AVAILABLE
184	6	L04	LOWER_HALL	AVAILABLE
185	6	L05	LOWER_HALL	AVAILABLE
186	6	L06	LOWER_HALL	AVAILABLE
187	6	L07	LOWER_HALL	AVAILABLE
188	6	L08	LOWER_HALL	AVAILABLE
189	6	L09	LOWER_HALL	AVAILABLE
190	6	L10	LOWER_HALL	AVAILABLE
191	6	L11	LOWER_HALL	AVAILABLE
192	6	L12	LOWER_HALL	AVAILABLE
193	6	L13	LOWER_HALL	AVAILABLE
194	6	L14	LOWER_HALL	AVAILABLE
195	6	L15	LOWER_HALL	AVAILABLE
196	6	L16	LOWER_HALL	AVAILABLE
197	6	L17	LOWER_HALL	AVAILABLE
198	6	L18	LOWER_HALL	AVAILABLE
199	6	L19	LOWER_HALL	AVAILABLE
200	6	L20	LOWER_HALL	AVAILABLE
201	6	L21	LOWER_HALL	AVAILABLE
202	6	L22	LOWER_HALL	AVAILABLE
203	6	L23	LOWER_HALL	AVAILABLE
204	6	L24	LOWER_HALL	AVAILABLE
205	6	L25	LOWER_HALL	AVAILABLE
206	6	L26	LOWER_HALL	AVAILABLE
207	6	L27	LOWER_HALL	AVAILABLE
208	6	L28	LOWER_HALL	AVAILABLE
209	6	L29	LOWER_HALL	AVAILABLE
210	6	L30	LOWER_HALL	AVAILABLE
211	6	U01	UPPER_GALLERY	AVAILABLE
212	6	U02	UPPER_GALLERY	AVAILABLE
213	6	U03	UPPER_GALLERY	AVAILABLE
214	6	U04	UPPER_GALLERY	AVAILABLE
215	6	U05	UPPER_GALLERY	AVAILABLE
216	6	U06	UPPER_GALLERY	AVAILABLE
217	6	U07	UPPER_GALLERY	AVAILABLE
218	6	U08	UPPER_GALLERY	AVAILABLE
219	6	U09	UPPER_GALLERY	AVAILABLE
220	6	U10	UPPER_GALLERY	AVAILABLE
221	6	U11	UPPER_GALLERY	AVAILABLE
222	6	U12	UPPER_GALLERY	AVAILABLE
223	6	U13	UPPER_GALLERY	AVAILABLE
224	6	U14	UPPER_GALLERY	AVAILABLE
225	6	U15	UPPER_GALLERY	AVAILABLE
226	6	U16	UPPER_GALLERY	AVAILABLE
227	6	U17	UPPER_GALLERY	AVAILABLE
228	6	U18	UPPER_GALLERY	AVAILABLE
229	6	U19	UPPER_GALLERY	AVAILABLE
230	6	U20	UPPER_GALLERY	AVAILABLE
231	6	U21	UPPER_GALLERY	AVAILABLE
232	6	U22	UPPER_GALLERY	AVAILABLE
233	6	U23	UPPER_GALLERY	AVAILABLE
234	6	U24	UPPER_GALLERY	AVAILABLE
235	6	U25	UPPER_GALLERY	AVAILABLE
236	6	U26	UPPER_GALLERY	AVAILABLE
237	6	U27	UPPER_GALLERY	AVAILABLE
238	6	U28	UPPER_GALLERY	AVAILABLE
239	6	U29	UPPER_GALLERY	AVAILABLE
240	6	U30	UPPER_GALLERY	AVAILABLE
241	6	U31	UPPER_GALLERY	AVAILABLE
242	6	U32	UPPER_GALLERY	AVAILABLE
243	6	U33	UPPER_GALLERY	AVAILABLE
244	6	U34	UPPER_GALLERY	AVAILABLE
245	6	U35	UPPER_GALLERY	AVAILABLE
246	6	U36	UPPER_GALLERY	AVAILABLE
247	6	U37	UPPER_GALLERY	AVAILABLE
248	6	U38	UPPER_GALLERY	AVAILABLE
249	6	U39	UPPER_GALLERY	AVAILABLE
250	6	U40	UPPER_GALLERY	AVAILABLE
251	6	U41	UPPER_GALLERY	AVAILABLE
252	6	U42	UPPER_GALLERY	AVAILABLE
253	6	U43	UPPER_GALLERY	AVAILABLE
254	6	U44	UPPER_GALLERY	AVAILABLE
255	6	U45	UPPER_GALLERY	AVAILABLE
256	6	U46	UPPER_GALLERY	AVAILABLE
257	6	U47	UPPER_GALLERY	AVAILABLE
258	6	U48	UPPER_GALLERY	AVAILABLE
259	6	U49	UPPER_GALLERY	AVAILABLE
260	6	U50	UPPER_GALLERY	AVAILABLE
261	6	U51	UPPER_GALLERY	AVAILABLE
262	6	U52	UPPER_GALLERY	AVAILABLE
263	6	U53	UPPER_GALLERY	AVAILABLE
264	6	U54	UPPER_GALLERY	AVAILABLE
265	6	U55	UPPER_GALLERY	AVAILABLE
266	6	U56	UPPER_GALLERY	AVAILABLE
267	6	U57	UPPER_GALLERY	AVAILABLE
268	6	U58	UPPER_GALLERY	AVAILABLE
269	6	U59	UPPER_GALLERY	AVAILABLE
270	6	U60	UPPER_GALLERY	AVAILABLE
271	6	V01	VIP	AVAILABLE
272	6	V02	VIP	AVAILABLE
273	6	V03	VIP	AVAILABLE
274	6	V04	VIP	AVAILABLE
275	6	V05	VIP	AVAILABLE
276	6	V06	VIP	AVAILABLE
277	6	V07	VIP	AVAILABLE
278	6	V08	VIP	AVAILABLE
279	6	V09	VIP	AVAILABLE
280	6	V10	VIP	AVAILABLE
281	7	L01	LOWER_HALL	AVAILABLE
282	7	L02	LOWER_HALL	AVAILABLE
283	7	L03	LOWER_HALL	AVAILABLE
284	7	L04	LOWER_HALL	AVAILABLE
285	7	L05	LOWER_HALL	AVAILABLE
286	7	L06	LOWER_HALL	AVAILABLE
287	7	L07	LOWER_HALL	AVAILABLE
288	7	L08	LOWER_HALL	AVAILABLE
289	7	L09	LOWER_HALL	AVAILABLE
290	7	L10	LOWER_HALL	AVAILABLE
291	7	L11	LOWER_HALL	AVAILABLE
292	7	L12	LOWER_HALL	AVAILABLE
293	7	L13	LOWER_HALL	AVAILABLE
294	7	L14	LOWER_HALL	AVAILABLE
295	7	L15	LOWER_HALL	AVAILABLE
296	7	L16	LOWER_HALL	AVAILABLE
297	7	L17	LOWER_HALL	AVAILABLE
298	7	L18	LOWER_HALL	AVAILABLE
299	7	L19	LOWER_HALL	AVAILABLE
300	7	L20	LOWER_HALL	AVAILABLE
301	7	L21	LOWER_HALL	AVAILABLE
302	7	L22	LOWER_HALL	AVAILABLE
303	7	L23	LOWER_HALL	AVAILABLE
304	7	L24	LOWER_HALL	AVAILABLE
305	7	L25	LOWER_HALL	AVAILABLE
306	7	L26	LOWER_HALL	AVAILABLE
307	7	L27	LOWER_HALL	AVAILABLE
308	7	L28	LOWER_HALL	AVAILABLE
309	7	L29	LOWER_HALL	AVAILABLE
310	7	L30	LOWER_HALL	AVAILABLE
311	7	U01	UPPER_GALLERY	AVAILABLE
312	7	U02	UPPER_GALLERY	AVAILABLE
313	7	U03	UPPER_GALLERY	AVAILABLE
314	7	U04	UPPER_GALLERY	AVAILABLE
315	7	U05	UPPER_GALLERY	AVAILABLE
316	7	U06	UPPER_GALLERY	AVAILABLE
317	7	U07	UPPER_GALLERY	AVAILABLE
318	7	U08	UPPER_GALLERY	AVAILABLE
319	7	U09	UPPER_GALLERY	AVAILABLE
320	7	U10	UPPER_GALLERY	AVAILABLE
321	7	U11	UPPER_GALLERY	AVAILABLE
322	7	U12	UPPER_GALLERY	AVAILABLE
323	7	U13	UPPER_GALLERY	AVAILABLE
324	7	U14	UPPER_GALLERY	AVAILABLE
325	7	U15	UPPER_GALLERY	AVAILABLE
326	7	U16	UPPER_GALLERY	AVAILABLE
327	7	U17	UPPER_GALLERY	AVAILABLE
328	7	U18	UPPER_GALLERY	AVAILABLE
329	7	U19	UPPER_GALLERY	AVAILABLE
330	7	U20	UPPER_GALLERY	AVAILABLE
331	7	U21	UPPER_GALLERY	AVAILABLE
332	7	U22	UPPER_GALLERY	AVAILABLE
333	7	U23	UPPER_GALLERY	AVAILABLE
334	7	U24	UPPER_GALLERY	AVAILABLE
335	7	U25	UPPER_GALLERY	AVAILABLE
336	7	U26	UPPER_GALLERY	AVAILABLE
337	7	U27	UPPER_GALLERY	AVAILABLE
338	7	U28	UPPER_GALLERY	AVAILABLE
339	7	U29	UPPER_GALLERY	AVAILABLE
340	7	U30	UPPER_GALLERY	AVAILABLE
341	7	U31	UPPER_GALLERY	AVAILABLE
342	7	U32	UPPER_GALLERY	AVAILABLE
343	7	U33	UPPER_GALLERY	AVAILABLE
344	7	U34	UPPER_GALLERY	AVAILABLE
345	7	U35	UPPER_GALLERY	AVAILABLE
346	7	U36	UPPER_GALLERY	AVAILABLE
347	7	U37	UPPER_GALLERY	AVAILABLE
348	7	U38	UPPER_GALLERY	AVAILABLE
349	7	U39	UPPER_GALLERY	AVAILABLE
350	7	U40	UPPER_GALLERY	AVAILABLE
351	7	U41	UPPER_GALLERY	AVAILABLE
352	7	U42	UPPER_GALLERY	AVAILABLE
353	7	U43	UPPER_GALLERY	AVAILABLE
354	7	U44	UPPER_GALLERY	AVAILABLE
355	7	U45	UPPER_GALLERY	AVAILABLE
356	7	U46	UPPER_GALLERY	AVAILABLE
357	7	U47	UPPER_GALLERY	AVAILABLE
358	7	U48	UPPER_GALLERY	AVAILABLE
359	7	U49	UPPER_GALLERY	AVAILABLE
360	7	U50	UPPER_GALLERY	AVAILABLE
361	7	U51	UPPER_GALLERY	AVAILABLE
362	7	U52	UPPER_GALLERY	AVAILABLE
363	7	U53	UPPER_GALLERY	AVAILABLE
364	7	U54	UPPER_GALLERY	AVAILABLE
365	7	U55	UPPER_GALLERY	AVAILABLE
366	7	U56	UPPER_GALLERY	AVAILABLE
367	7	U57	UPPER_GALLERY	AVAILABLE
368	7	U58	UPPER_GALLERY	AVAILABLE
369	7	U59	UPPER_GALLERY	AVAILABLE
370	7	U60	UPPER_GALLERY	AVAILABLE
371	7	V01	VIP	AVAILABLE
372	7	V02	VIP	AVAILABLE
373	7	V03	VIP	AVAILABLE
374	7	V04	VIP	AVAILABLE
375	7	V05	VIP	AVAILABLE
376	7	V06	VIP	AVAILABLE
377	7	V07	VIP	AVAILABLE
378	7	V08	VIP	AVAILABLE
379	7	V09	VIP	AVAILABLE
380	7	V10	VIP	AVAILABLE
381	8	L01	LOWER_HALL	AVAILABLE
382	8	L02	LOWER_HALL	AVAILABLE
383	8	L03	LOWER_HALL	AVAILABLE
384	8	L04	LOWER_HALL	AVAILABLE
385	8	L05	LOWER_HALL	AVAILABLE
386	8	L06	LOWER_HALL	AVAILABLE
387	8	L07	LOWER_HALL	AVAILABLE
388	8	L08	LOWER_HALL	AVAILABLE
389	8	L09	LOWER_HALL	AVAILABLE
390	8	L10	LOWER_HALL	AVAILABLE
391	8	L11	LOWER_HALL	AVAILABLE
392	8	L12	LOWER_HALL	AVAILABLE
393	8	L13	LOWER_HALL	AVAILABLE
394	8	L14	LOWER_HALL	AVAILABLE
395	8	L15	LOWER_HALL	AVAILABLE
396	8	L16	LOWER_HALL	AVAILABLE
397	8	L17	LOWER_HALL	AVAILABLE
398	8	L18	LOWER_HALL	AVAILABLE
399	8	L19	LOWER_HALL	AVAILABLE
400	8	L20	LOWER_HALL	AVAILABLE
401	8	L21	LOWER_HALL	AVAILABLE
402	8	L22	LOWER_HALL	AVAILABLE
403	8	L23	LOWER_HALL	AVAILABLE
404	8	L24	LOWER_HALL	AVAILABLE
405	8	L25	LOWER_HALL	AVAILABLE
406	8	L26	LOWER_HALL	AVAILABLE
407	8	L27	LOWER_HALL	AVAILABLE
408	8	L28	LOWER_HALL	AVAILABLE
409	8	L29	LOWER_HALL	AVAILABLE
410	8	L30	LOWER_HALL	AVAILABLE
411	8	U01	UPPER_GALLERY	AVAILABLE
412	8	U02	UPPER_GALLERY	AVAILABLE
413	8	U03	UPPER_GALLERY	AVAILABLE
414	8	U04	UPPER_GALLERY	AVAILABLE
415	8	U05	UPPER_GALLERY	AVAILABLE
416	8	U06	UPPER_GALLERY	AVAILABLE
417	8	U07	UPPER_GALLERY	AVAILABLE
418	8	U08	UPPER_GALLERY	AVAILABLE
419	8	U09	UPPER_GALLERY	AVAILABLE
420	8	U10	UPPER_GALLERY	AVAILABLE
421	8	U11	UPPER_GALLERY	AVAILABLE
422	8	U12	UPPER_GALLERY	AVAILABLE
423	8	U13	UPPER_GALLERY	AVAILABLE
424	8	U14	UPPER_GALLERY	AVAILABLE
425	8	U15	UPPER_GALLERY	AVAILABLE
426	8	U16	UPPER_GALLERY	AVAILABLE
427	8	U17	UPPER_GALLERY	AVAILABLE
428	8	U18	UPPER_GALLERY	AVAILABLE
429	8	U19	UPPER_GALLERY	AVAILABLE
430	8	U20	UPPER_GALLERY	AVAILABLE
431	8	U21	UPPER_GALLERY	AVAILABLE
432	8	U22	UPPER_GALLERY	AVAILABLE
433	8	U23	UPPER_GALLERY	AVAILABLE
434	8	U24	UPPER_GALLERY	AVAILABLE
435	8	U25	UPPER_GALLERY	AVAILABLE
436	8	U26	UPPER_GALLERY	AVAILABLE
437	8	U27	UPPER_GALLERY	AVAILABLE
438	8	U28	UPPER_GALLERY	AVAILABLE
439	8	U29	UPPER_GALLERY	AVAILABLE
440	8	U30	UPPER_GALLERY	AVAILABLE
441	8	U31	UPPER_GALLERY	AVAILABLE
442	8	U32	UPPER_GALLERY	AVAILABLE
443	8	U33	UPPER_GALLERY	AVAILABLE
444	8	U34	UPPER_GALLERY	AVAILABLE
445	8	U35	UPPER_GALLERY	AVAILABLE
446	8	U36	UPPER_GALLERY	AVAILABLE
447	8	U37	UPPER_GALLERY	AVAILABLE
448	8	U38	UPPER_GALLERY	AVAILABLE
449	8	U39	UPPER_GALLERY	AVAILABLE
450	8	U40	UPPER_GALLERY	AVAILABLE
451	8	U41	UPPER_GALLERY	AVAILABLE
452	8	U42	UPPER_GALLERY	AVAILABLE
453	8	U43	UPPER_GALLERY	AVAILABLE
454	8	U44	UPPER_GALLERY	AVAILABLE
455	8	U45	UPPER_GALLERY	AVAILABLE
456	8	U46	UPPER_GALLERY	AVAILABLE
457	8	U47	UPPER_GALLERY	AVAILABLE
458	8	U48	UPPER_GALLERY	AVAILABLE
459	8	U49	UPPER_GALLERY	AVAILABLE
460	8	U50	UPPER_GALLERY	AVAILABLE
461	8	U51	UPPER_GALLERY	AVAILABLE
462	8	U52	UPPER_GALLERY	AVAILABLE
463	8	U53	UPPER_GALLERY	AVAILABLE
464	8	U54	UPPER_GALLERY	AVAILABLE
465	8	U55	UPPER_GALLERY	AVAILABLE
466	8	U56	UPPER_GALLERY	AVAILABLE
467	8	U57	UPPER_GALLERY	AVAILABLE
468	8	U58	UPPER_GALLERY	AVAILABLE
469	8	U59	UPPER_GALLERY	AVAILABLE
470	8	U60	UPPER_GALLERY	AVAILABLE
471	8	V01	VIP	AVAILABLE
472	8	V02	VIP	AVAILABLE
473	8	V03	VIP	AVAILABLE
474	8	V04	VIP	AVAILABLE
475	8	V05	VIP	AVAILABLE
476	8	V06	VIP	AVAILABLE
477	8	V07	VIP	AVAILABLE
478	8	V08	VIP	AVAILABLE
479	8	V09	VIP	AVAILABLE
480	8	V10	VIP	AVAILABLE
481	9	L01	LOWER_HALL	AVAILABLE
482	9	L02	LOWER_HALL	AVAILABLE
483	9	L03	LOWER_HALL	AVAILABLE
484	9	L04	LOWER_HALL	AVAILABLE
485	9	L05	LOWER_HALL	AVAILABLE
486	9	L06	LOWER_HALL	AVAILABLE
487	9	L07	LOWER_HALL	AVAILABLE
488	9	L08	LOWER_HALL	AVAILABLE
489	9	L09	LOWER_HALL	AVAILABLE
490	9	L10	LOWER_HALL	AVAILABLE
491	9	L11	LOWER_HALL	AVAILABLE
492	9	L12	LOWER_HALL	AVAILABLE
493	9	L13	LOWER_HALL	AVAILABLE
494	9	L14	LOWER_HALL	AVAILABLE
495	9	L15	LOWER_HALL	AVAILABLE
496	9	L16	LOWER_HALL	AVAILABLE
497	9	L17	LOWER_HALL	AVAILABLE
498	9	L18	LOWER_HALL	AVAILABLE
499	9	L19	LOWER_HALL	AVAILABLE
500	9	L20	LOWER_HALL	AVAILABLE
501	9	L21	LOWER_HALL	AVAILABLE
502	9	L22	LOWER_HALL	AVAILABLE
503	9	L23	LOWER_HALL	AVAILABLE
504	9	L24	LOWER_HALL	AVAILABLE
505	9	L25	LOWER_HALL	AVAILABLE
506	9	L26	LOWER_HALL	AVAILABLE
507	9	L27	LOWER_HALL	AVAILABLE
508	9	L28	LOWER_HALL	AVAILABLE
509	9	L29	LOWER_HALL	AVAILABLE
510	9	L30	LOWER_HALL	AVAILABLE
511	9	U01	UPPER_GALLERY	AVAILABLE
512	9	U02	UPPER_GALLERY	AVAILABLE
513	9	U03	UPPER_GALLERY	AVAILABLE
514	9	U04	UPPER_GALLERY	AVAILABLE
515	9	U05	UPPER_GALLERY	AVAILABLE
516	9	U06	UPPER_GALLERY	AVAILABLE
517	9	U07	UPPER_GALLERY	AVAILABLE
518	9	U08	UPPER_GALLERY	AVAILABLE
519	9	U09	UPPER_GALLERY	AVAILABLE
520	9	U10	UPPER_GALLERY	AVAILABLE
521	9	U11	UPPER_GALLERY	AVAILABLE
522	9	U12	UPPER_GALLERY	AVAILABLE
523	9	U13	UPPER_GALLERY	AVAILABLE
524	9	U14	UPPER_GALLERY	AVAILABLE
525	9	U15	UPPER_GALLERY	AVAILABLE
526	9	U16	UPPER_GALLERY	AVAILABLE
527	9	U17	UPPER_GALLERY	AVAILABLE
528	9	U18	UPPER_GALLERY	AVAILABLE
529	9	U19	UPPER_GALLERY	AVAILABLE
530	9	U20	UPPER_GALLERY	AVAILABLE
531	9	U21	UPPER_GALLERY	AVAILABLE
532	9	U22	UPPER_GALLERY	AVAILABLE
533	9	U23	UPPER_GALLERY	AVAILABLE
534	9	U24	UPPER_GALLERY	AVAILABLE
535	9	U25	UPPER_GALLERY	AVAILABLE
536	9	U26	UPPER_GALLERY	AVAILABLE
537	9	U27	UPPER_GALLERY	AVAILABLE
538	9	U28	UPPER_GALLERY	AVAILABLE
539	9	U29	UPPER_GALLERY	AVAILABLE
540	9	U30	UPPER_GALLERY	AVAILABLE
541	9	U31	UPPER_GALLERY	AVAILABLE
542	9	U32	UPPER_GALLERY	AVAILABLE
543	9	U33	UPPER_GALLERY	AVAILABLE
544	9	U34	UPPER_GALLERY	AVAILABLE
545	9	U35	UPPER_GALLERY	AVAILABLE
546	9	U36	UPPER_GALLERY	AVAILABLE
547	9	U37	UPPER_GALLERY	AVAILABLE
548	9	U38	UPPER_GALLERY	AVAILABLE
549	9	U39	UPPER_GALLERY	AVAILABLE
550	9	U40	UPPER_GALLERY	AVAILABLE
551	9	U41	UPPER_GALLERY	AVAILABLE
552	9	U42	UPPER_GALLERY	AVAILABLE
553	9	U43	UPPER_GALLERY	AVAILABLE
554	9	U44	UPPER_GALLERY	AVAILABLE
555	9	U45	UPPER_GALLERY	AVAILABLE
556	9	U46	UPPER_GALLERY	AVAILABLE
557	9	U47	UPPER_GALLERY	AVAILABLE
558	9	U48	UPPER_GALLERY	AVAILABLE
559	9	U49	UPPER_GALLERY	AVAILABLE
560	9	U50	UPPER_GALLERY	AVAILABLE
561	9	U51	UPPER_GALLERY	AVAILABLE
562	9	U52	UPPER_GALLERY	AVAILABLE
563	9	U53	UPPER_GALLERY	AVAILABLE
564	9	U54	UPPER_GALLERY	AVAILABLE
565	9	U55	UPPER_GALLERY	AVAILABLE
566	9	U56	UPPER_GALLERY	AVAILABLE
567	9	U57	UPPER_GALLERY	AVAILABLE
568	9	U58	UPPER_GALLERY	AVAILABLE
569	9	U59	UPPER_GALLERY	AVAILABLE
570	9	U60	UPPER_GALLERY	AVAILABLE
571	9	V01	VIP	AVAILABLE
572	9	V02	VIP	AVAILABLE
573	9	V03	VIP	AVAILABLE
574	9	V04	VIP	AVAILABLE
575	9	V05	VIP	AVAILABLE
576	9	V06	VIP	AVAILABLE
577	9	V07	VIP	AVAILABLE
578	9	V08	VIP	AVAILABLE
579	9	V09	VIP	AVAILABLE
580	9	V10	VIP	AVAILABLE
581	10	L01	LOWER_HALL	AVAILABLE
582	10	L02	LOWER_HALL	AVAILABLE
583	10	L03	LOWER_HALL	AVAILABLE
584	10	L04	LOWER_HALL	AVAILABLE
585	10	L05	LOWER_HALL	AVAILABLE
586	10	L06	LOWER_HALL	AVAILABLE
587	10	L07	LOWER_HALL	AVAILABLE
588	10	L08	LOWER_HALL	AVAILABLE
589	10	L09	LOWER_HALL	AVAILABLE
590	10	L10	LOWER_HALL	AVAILABLE
591	10	L11	LOWER_HALL	AVAILABLE
592	10	L12	LOWER_HALL	AVAILABLE
593	10	L13	LOWER_HALL	AVAILABLE
594	10	L14	LOWER_HALL	AVAILABLE
595	10	L15	LOWER_HALL	AVAILABLE
596	10	L16	LOWER_HALL	AVAILABLE
597	10	L17	LOWER_HALL	AVAILABLE
598	10	L18	LOWER_HALL	AVAILABLE
599	10	L19	LOWER_HALL	AVAILABLE
600	10	L20	LOWER_HALL	AVAILABLE
601	10	L21	LOWER_HALL	AVAILABLE
602	10	L22	LOWER_HALL	AVAILABLE
603	10	L23	LOWER_HALL	AVAILABLE
604	10	L24	LOWER_HALL	AVAILABLE
605	10	L25	LOWER_HALL	AVAILABLE
606	10	L26	LOWER_HALL	AVAILABLE
607	10	L27	LOWER_HALL	AVAILABLE
608	10	L28	LOWER_HALL	AVAILABLE
609	10	L29	LOWER_HALL	AVAILABLE
610	10	L30	LOWER_HALL	AVAILABLE
611	10	U01	UPPER_GALLERY	AVAILABLE
612	10	U02	UPPER_GALLERY	AVAILABLE
613	10	U03	UPPER_GALLERY	AVAILABLE
614	10	U04	UPPER_GALLERY	AVAILABLE
615	10	U05	UPPER_GALLERY	AVAILABLE
616	10	U06	UPPER_GALLERY	AVAILABLE
617	10	U07	UPPER_GALLERY	AVAILABLE
618	10	U08	UPPER_GALLERY	AVAILABLE
619	10	U09	UPPER_GALLERY	AVAILABLE
620	10	U10	UPPER_GALLERY	AVAILABLE
621	10	U11	UPPER_GALLERY	AVAILABLE
622	10	U12	UPPER_GALLERY	AVAILABLE
623	10	U13	UPPER_GALLERY	AVAILABLE
624	10	U14	UPPER_GALLERY	AVAILABLE
625	10	U15	UPPER_GALLERY	AVAILABLE
626	10	U16	UPPER_GALLERY	AVAILABLE
627	10	U17	UPPER_GALLERY	AVAILABLE
628	10	U18	UPPER_GALLERY	AVAILABLE
629	10	U19	UPPER_GALLERY	AVAILABLE
630	10	U20	UPPER_GALLERY	AVAILABLE
631	10	U21	UPPER_GALLERY	AVAILABLE
632	10	U22	UPPER_GALLERY	AVAILABLE
633	10	U23	UPPER_GALLERY	AVAILABLE
634	10	U24	UPPER_GALLERY	AVAILABLE
635	10	U25	UPPER_GALLERY	AVAILABLE
636	10	U26	UPPER_GALLERY	AVAILABLE
637	10	U27	UPPER_GALLERY	AVAILABLE
638	10	U28	UPPER_GALLERY	AVAILABLE
639	10	U29	UPPER_GALLERY	AVAILABLE
640	10	U30	UPPER_GALLERY	AVAILABLE
641	10	U31	UPPER_GALLERY	AVAILABLE
642	10	U32	UPPER_GALLERY	AVAILABLE
643	10	U33	UPPER_GALLERY	AVAILABLE
644	10	U34	UPPER_GALLERY	AVAILABLE
645	10	U35	UPPER_GALLERY	AVAILABLE
646	10	U36	UPPER_GALLERY	AVAILABLE
647	10	U37	UPPER_GALLERY	AVAILABLE
648	10	U38	UPPER_GALLERY	AVAILABLE
649	10	U39	UPPER_GALLERY	AVAILABLE
650	10	U40	UPPER_GALLERY	AVAILABLE
651	10	U41	UPPER_GALLERY	AVAILABLE
652	10	U42	UPPER_GALLERY	AVAILABLE
653	10	U43	UPPER_GALLERY	AVAILABLE
654	10	U44	UPPER_GALLERY	AVAILABLE
655	10	U45	UPPER_GALLERY	AVAILABLE
656	10	U46	UPPER_GALLERY	AVAILABLE
657	10	U47	UPPER_GALLERY	AVAILABLE
658	10	U48	UPPER_GALLERY	AVAILABLE
659	10	U49	UPPER_GALLERY	AVAILABLE
660	10	U50	UPPER_GALLERY	AVAILABLE
661	10	U51	UPPER_GALLERY	AVAILABLE
662	10	U52	UPPER_GALLERY	AVAILABLE
663	10	U53	UPPER_GALLERY	AVAILABLE
664	10	U54	UPPER_GALLERY	AVAILABLE
665	10	U55	UPPER_GALLERY	AVAILABLE
666	10	U56	UPPER_GALLERY	AVAILABLE
667	10	U57	UPPER_GALLERY	AVAILABLE
668	10	U58	UPPER_GALLERY	AVAILABLE
669	10	U59	UPPER_GALLERY	AVAILABLE
670	10	U60	UPPER_GALLERY	AVAILABLE
671	10	V01	VIP	AVAILABLE
672	10	V02	VIP	AVAILABLE
673	10	V03	VIP	AVAILABLE
674	10	V04	VIP	AVAILABLE
675	10	V05	VIP	AVAILABLE
676	10	V06	VIP	AVAILABLE
677	10	V07	VIP	AVAILABLE
678	10	V08	VIP	AVAILABLE
679	10	V09	VIP	AVAILABLE
680	10	V10	VIP	AVAILABLE
681	11	L01	LOWER_HALL	AVAILABLE
682	11	L02	LOWER_HALL	AVAILABLE
683	11	L03	LOWER_HALL	AVAILABLE
684	11	L04	LOWER_HALL	AVAILABLE
685	11	L05	LOWER_HALL	AVAILABLE
686	11	L06	LOWER_HALL	AVAILABLE
687	11	L07	LOWER_HALL	AVAILABLE
688	11	L08	LOWER_HALL	AVAILABLE
689	11	L09	LOWER_HALL	AVAILABLE
690	11	L10	LOWER_HALL	AVAILABLE
691	11	L11	LOWER_HALL	AVAILABLE
692	11	L12	LOWER_HALL	AVAILABLE
693	11	L13	LOWER_HALL	AVAILABLE
694	11	L14	LOWER_HALL	AVAILABLE
695	11	L15	LOWER_HALL	AVAILABLE
696	11	L16	LOWER_HALL	AVAILABLE
697	11	L17	LOWER_HALL	AVAILABLE
698	11	L18	LOWER_HALL	AVAILABLE
699	11	L19	LOWER_HALL	AVAILABLE
700	11	L20	LOWER_HALL	AVAILABLE
701	11	L21	LOWER_HALL	AVAILABLE
702	11	L22	LOWER_HALL	AVAILABLE
703	11	L23	LOWER_HALL	AVAILABLE
704	11	L24	LOWER_HALL	AVAILABLE
705	11	L25	LOWER_HALL	AVAILABLE
706	11	L26	LOWER_HALL	AVAILABLE
707	11	L27	LOWER_HALL	AVAILABLE
708	11	L28	LOWER_HALL	AVAILABLE
709	11	L29	LOWER_HALL	AVAILABLE
710	11	L30	LOWER_HALL	AVAILABLE
711	11	U01	UPPER_GALLERY	AVAILABLE
712	11	U02	UPPER_GALLERY	AVAILABLE
713	11	U03	UPPER_GALLERY	AVAILABLE
714	11	U04	UPPER_GALLERY	AVAILABLE
715	11	U05	UPPER_GALLERY	AVAILABLE
716	11	U06	UPPER_GALLERY	AVAILABLE
717	11	U07	UPPER_GALLERY	AVAILABLE
718	11	U08	UPPER_GALLERY	AVAILABLE
719	11	U09	UPPER_GALLERY	AVAILABLE
720	11	U10	UPPER_GALLERY	AVAILABLE
721	11	U11	UPPER_GALLERY	AVAILABLE
722	11	U12	UPPER_GALLERY	AVAILABLE
723	11	U13	UPPER_GALLERY	AVAILABLE
724	11	U14	UPPER_GALLERY	AVAILABLE
725	11	U15	UPPER_GALLERY	AVAILABLE
726	11	U16	UPPER_GALLERY	AVAILABLE
727	11	U17	UPPER_GALLERY	AVAILABLE
728	11	U18	UPPER_GALLERY	AVAILABLE
729	11	U19	UPPER_GALLERY	AVAILABLE
730	11	U20	UPPER_GALLERY	AVAILABLE
731	11	U21	UPPER_GALLERY	AVAILABLE
732	11	U22	UPPER_GALLERY	AVAILABLE
733	11	U23	UPPER_GALLERY	AVAILABLE
734	11	U24	UPPER_GALLERY	AVAILABLE
735	11	U25	UPPER_GALLERY	AVAILABLE
736	11	U26	UPPER_GALLERY	AVAILABLE
737	11	U27	UPPER_GALLERY	AVAILABLE
738	11	U28	UPPER_GALLERY	AVAILABLE
739	11	U29	UPPER_GALLERY	AVAILABLE
740	11	U30	UPPER_GALLERY	AVAILABLE
741	11	U31	UPPER_GALLERY	AVAILABLE
742	11	U32	UPPER_GALLERY	AVAILABLE
743	11	U33	UPPER_GALLERY	AVAILABLE
744	11	U34	UPPER_GALLERY	AVAILABLE
745	11	U35	UPPER_GALLERY	AVAILABLE
746	11	U36	UPPER_GALLERY	AVAILABLE
747	11	U37	UPPER_GALLERY	AVAILABLE
748	11	U38	UPPER_GALLERY	AVAILABLE
749	11	U39	UPPER_GALLERY	AVAILABLE
750	11	U40	UPPER_GALLERY	AVAILABLE
751	11	U41	UPPER_GALLERY	AVAILABLE
752	11	U42	UPPER_GALLERY	AVAILABLE
753	11	U43	UPPER_GALLERY	AVAILABLE
754	11	U44	UPPER_GALLERY	AVAILABLE
755	11	U45	UPPER_GALLERY	AVAILABLE
756	11	U46	UPPER_GALLERY	AVAILABLE
757	11	U47	UPPER_GALLERY	AVAILABLE
758	11	U48	UPPER_GALLERY	AVAILABLE
759	11	U49	UPPER_GALLERY	AVAILABLE
760	11	U50	UPPER_GALLERY	AVAILABLE
761	11	U51	UPPER_GALLERY	AVAILABLE
762	11	U52	UPPER_GALLERY	AVAILABLE
763	11	U53	UPPER_GALLERY	AVAILABLE
764	11	U54	UPPER_GALLERY	AVAILABLE
765	11	U55	UPPER_GALLERY	AVAILABLE
766	11	U56	UPPER_GALLERY	AVAILABLE
767	11	U57	UPPER_GALLERY	AVAILABLE
768	11	U58	UPPER_GALLERY	AVAILABLE
769	11	U59	UPPER_GALLERY	AVAILABLE
770	11	U60	UPPER_GALLERY	AVAILABLE
771	11	V01	VIP	AVAILABLE
772	11	V02	VIP	AVAILABLE
773	11	V03	VIP	AVAILABLE
774	11	V04	VIP	AVAILABLE
775	11	V05	VIP	AVAILABLE
776	11	V06	VIP	AVAILABLE
777	11	V07	VIP	AVAILABLE
778	11	V08	VIP	AVAILABLE
779	11	V09	VIP	AVAILABLE
780	11	V10	VIP	AVAILABLE
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, password_hash, full_name, email, role, assigned_cinema_id) FROM stdin;
1	jsmith	ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f	James Smith	jsmith@horizon.com	BOOKING_STAFF	3
2	mlopez	ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f	Maria Lopez	mlopez@horizon.com	BOOKING_STAFF	3
3	apatel	ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f	Amit Patel	apatel@horizon.com	BOOKING_STAFF	1
4	sadmin	ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f	Sarah Admin	sadmin@horizon.com	ADMIN	\N
5	badmin	ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f	Bob Admin	badmin@horizon.com	ADMIN	\N
6	mmanager	ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f	Mike Manager	mmanager@horizon.com	MANAGER	\N
7	girish	a3d16ffbc1e878618b9f42281074602e7ed8c4bf36b5416fa965f34ae1fbafec	Girish Shah	girish@gmail.com	BOOKING_STAFF	3
8	bibidh	240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9	bibidh test	bibdh@gmail.com	ADMIN	\N
\.


--
-- Name: booking_booking_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.booking_booking_id_seq', 12, true);


--
-- Name: cinema_cinema_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cinema_cinema_id_seq', 8, true);


--
-- Name: city_city_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.city_city_id_seq', 4, true);


--
-- Name: customer_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customer_customer_id_seq', 10, true);


--
-- Name: film_film_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.film_film_id_seq', 6, true);


--
-- Name: listing_listing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.listing_listing_id_seq', 17, true);


--
-- Name: pricing_policy_policy_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pricing_policy_policy_id_seq', 4, true);


--
-- Name: receipt_receipt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.receipt_receipt_id_seq', 11, true);


--
-- Name: screen_screen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.screen_screen_id_seq', 11, true);


--
-- Name: seat_seat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seat_seat_id_seq', 780, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 8, true);


--
-- Name: booking booking_booking_reference_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_booking_reference_key UNIQUE (booking_reference);


--
-- Name: booking booking_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_pkey PRIMARY KEY (booking_id);


--
-- Name: booking_seat booking_seat_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking_seat
    ADD CONSTRAINT booking_seat_pkey PRIMARY KEY (booking_id, seat_id);


--
-- Name: cinema cinema_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cinema
    ADD CONSTRAINT cinema_pkey PRIMARY KEY (cinema_id);


--
-- Name: city city_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.city
    ADD CONSTRAINT city_pkey PRIMARY KEY (city_id);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (customer_id);


--
-- Name: film film_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.film
    ADD CONSTRAINT film_pkey PRIMARY KEY (film_id);


--
-- Name: listing listing_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listing
    ADD CONSTRAINT listing_pkey PRIMARY KEY (listing_id);


--
-- Name: pricing_policy pricing_policy_city_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pricing_policy
    ADD CONSTRAINT pricing_policy_city_id_key UNIQUE (city_id);


--
-- Name: pricing_policy pricing_policy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pricing_policy
    ADD CONSTRAINT pricing_policy_pkey PRIMARY KEY (policy_id);


--
-- Name: receipt receipt_booking_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.receipt
    ADD CONSTRAINT receipt_booking_id_key UNIQUE (booking_id);


--
-- Name: receipt receipt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.receipt
    ADD CONSTRAINT receipt_pkey PRIMARY KEY (receipt_id);


--
-- Name: screen screen_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.screen
    ADD CONSTRAINT screen_pkey PRIMARY KEY (screen_id);


--
-- Name: seat seat_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seat
    ADD CONSTRAINT seat_pkey PRIMARY KEY (seat_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: booking booking_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customer(customer_id);


--
-- Name: booking booking_listing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_listing_id_fkey FOREIGN KEY (listing_id) REFERENCES public.listing(listing_id);


--
-- Name: booking_seat booking_seat_booking_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking_seat
    ADD CONSTRAINT booking_seat_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES public.booking(booking_id) ON DELETE CASCADE;


--
-- Name: booking_seat booking_seat_seat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking_seat
    ADD CONSTRAINT booking_seat_seat_id_fkey FOREIGN KEY (seat_id) REFERENCES public.seat(seat_id);


--
-- Name: booking booking_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: cinema cinema_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cinema
    ADD CONSTRAINT cinema_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.city(city_id);


--
-- Name: listing listing_film_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listing
    ADD CONSTRAINT listing_film_id_fkey FOREIGN KEY (film_id) REFERENCES public.film(film_id);


--
-- Name: listing listing_screen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listing
    ADD CONSTRAINT listing_screen_id_fkey FOREIGN KEY (screen_id) REFERENCES public.screen(screen_id);


--
-- Name: pricing_policy pricing_policy_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pricing_policy
    ADD CONSTRAINT pricing_policy_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.city(city_id) ON DELETE CASCADE;


--
-- Name: receipt receipt_booking_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.receipt
    ADD CONSTRAINT receipt_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES public.booking(booking_id) ON DELETE CASCADE;


--
-- Name: screen screen_cinema_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.screen
    ADD CONSTRAINT screen_cinema_id_fkey FOREIGN KEY (cinema_id) REFERENCES public.cinema(cinema_id) ON DELETE CASCADE;


--
-- Name: seat seat_screen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seat
    ADD CONSTRAINT seat_screen_id_fkey FOREIGN KEY (screen_id) REFERENCES public.screen(screen_id) ON DELETE CASCADE;


--
-- Name: users users_assigned_cinema_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_assigned_cinema_id_fkey FOREIGN KEY (assigned_cinema_id) REFERENCES public.cinema(cinema_id);


--
-- PostgreSQL database dump complete
--

\unrestrict xI1PDhbXKeaV2jTudnI5nZgqtTiuva5UmQZB6EOfBc8FXkUAC9bpOOx32EyR17y

