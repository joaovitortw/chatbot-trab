--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-20 10:32:21

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
-- TOC entry 218 (class 1259 OID 16559)
-- Name: logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs (
    id integer NOT NULL,
    pergunta text NOT NULL,
    resposta text NOT NULL,
    ts timestamp without time zone NOT NULL
);


ALTER TABLE public.logs OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16558)
-- Name: logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.logs_id_seq OWNER TO postgres;

--
-- TOC entry 4897 (class 0 OID 0)
-- Dependencies: 217
-- Name: logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.logs_id_seq OWNED BY public.logs.id;


--
-- TOC entry 4742 (class 2604 OID 16562)
-- Name: logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs ALTER COLUMN id SET DEFAULT nextval('public.logs_id_seq'::regclass);


--
-- TOC entry 4891 (class 0 OID 16559)
-- Dependencies: 218
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs (id, pergunta, resposta, ts) FROM stdin;
1	Qual motor da ferrari 458?	O motor da Ferrari 458 é um V8 de 4.5 litros (4.497 ou 4.499 cm³ dependendo da fonte) da família "Ferrari/Maserati" F136. Ele produz entre 562 e 597 cavalos de potência (570 a 605 PS) dependendo da versão (Italia, Spider, Speciale). É um motor aspirado naturalmente, montado na posição central-traseira do carro.	2025-05-07 00:12:13.880451
2	Ficha tecnica c22ne	O motor C22NE é um motor a gasolina da Isuzu, com 2.2 ou 2.4 litros, dependendo da versão. Ele foi usado em diversos veículos, incluindo a série TF e o modelo KB240 (produzido entre 2004 e 2015). É conhecido por sua durabilidade. Existem manuais de oficina disponíveis para este motor, cobrindo diagnóstico, mecânica, arrefecimento, combustível, sistema elétrico e ignição.	2025-05-07 00:12:46.87765
3	carros c22ne	O C22NE é um motor 2.2 litros de 4 cilindros da família GM Family II, originalmente desenvolvido pela Opel. Ele foi utilizado em diversos carros, incluindo:\n\n*   **Opel Omega:** Um carro executivo fabricado pela Opel entre 1986 e 2003.\n*   **Opel Vectra:** Especificamente no Vectra B2 (e aparentemente em outros modelos Vectra 2.2 8v).\n*   **Isuzu TF Series:**  Indicado por um manual de serviço para motores a gasolina Isuzu TF Series.\n\nAparentemente, esse motor também foi usado (ou tem uma variante) em carros da Chevrolet e Isuzu, o que explica as referências a essas marcas junto com a Opel/GM.	2025-05-07 00:13:35.171191
4	c20xe	O C20XE é um motor 2.0L de 4 cilindros da família Family II da Opel, conhecido pelo seu potencial de alta performance. Era utilizado em diversos carros e é popular entre preparadores devido à facilidade de aumentar sua potência. Alguns exemplos de carros que o utilizavam são o Opel Kadett GSI e Vauxhall/Opel modelos.	2025-05-07 00:14:13.595097
5	Qual é o consumo médio de um Honda Civic?	Desculpe, não encontrei informações relevantes.	2025-05-14 00:47:51.668596
6	Qual a velocidade máxima de uma Ferrari 458?	Desculpe, não encontrei informações relevantes.	2025-05-14 00:47:55.139605
7	Qual é o consumo médio de um Honda Civic?	O consumo médio de um Honda Civic varia bastante dependendo do ano, modelo do motor e tipo de combustível (gasolina ou flex). Além disso, o consumo na cidade e na estrada também difere.\n\n**Em resumo:**\n\n*   **Modelos mais recentes (2.0 Flex):** Em torno de 10,5 km/l na cidade (gasolina).\n*   **Modelos mais antigos (2.0 Flex):** Podem variar entre 6,4 km/l (álcool) e 9,7 km/l (gasolina).\n*   **Modelos Si (2.4 Gasolina):** Consumo em torno de 8,3 km/l na cidade e 11,6 km/l na estrada.\n\nPara uma estimativa mais precisa, é fundamental que você especifique o ano e o modelo exato do Honda Civic que te interessa. Além disso, considere que o estilo de direção e as condições da via também influenciam no consumo real do veículo.	2025-05-14 00:49:39.386821
8	Qual a velocidade máxima de uma Ferrari 458?	A velocidade máxima da Ferrari 458 Italia é de aproximadamente 325 km/h (202 mph). A versão Spider atinge cerca de 320 km/h (199 mph), enquanto a 458 Speciale também alcança os 325 km/h (202 mph).	2025-05-14 00:49:49.281347
9	Qual é o consumo médio de um Honda Civic?	O consumo médio de um Honda Civic varia bastante dependendo do ano, modelo do motor, tipo de combustível (gasolina ou flex) e condições de uso (cidade ou estrada). No entanto, podemos generalizar da seguinte forma:\n\n*   **Na cidade:** O consumo varia entre 6,4 km/l (álcool em modelos flex) até 11,1 km/l (gasolina). A média fica em torno de 10,5 km/l para modelos com motor 2.0.\n*   **Na estrada:** O consumo pode variar de 11,6 km/l (gasolina) até impressionantes 21,9 km/l, dependendo do modelo e motorização.\n\nPara ter uma estimativa mais precisa, é importante especificar o ano e o modelo exato do Honda Civic em questão.	2025-05-14 01:07:47.00344
10	Qual a autonomia de um Tesla Model 3?	A autonomia de um Tesla Model 3 varia dependendo da versão e do ciclo de testes (WLTP). Aqui está um resumo:\n\n*   **Long Range (mais recente):** Até 702 km (ciclo WLTP).\n*   **Long Range (anterior):** Aproximadamente 580 km (dados de algumas fontes) ou 629 km (ciclo WLTP, segundo outra fonte).\n*   **Melhorias (modelo 2024):** Espera-se um aumento de até 12% na autonomia devido a melhorias na bateria e aerodinâmica.\n\nÉ importante notar que a autonomia real pode variar com base em fatores como estilo de condução, condições climáticas e uso do ar condicionado/aquecedor.	2025-05-14 01:08:43.772856
\.


--
-- TOC entry 4898 (class 0 OID 0)
-- Dependencies: 217
-- Name: logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.logs_id_seq', 10, true);


--
-- TOC entry 4744 (class 2606 OID 16566)
-- Name: logs logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);


-- Completed on 2025-05-20 10:32:22

--
-- PostgreSQL database dump complete
--

