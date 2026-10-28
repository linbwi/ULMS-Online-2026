# Software Requirements Specification

**Project:** University Library Management System Online (ULMS Online)
**Version:** 1.0
**Status:** Draft - for review
**Author:** Not specified
**Organization:** University Library
**Creation Date:** 2026-10-22

---

## 1. Introduction

### 1.1 Purpose

This document specifies the requirements for University Library Management System Online (ULMS Online). It provides a common reference for stakeholders, developers, testers, and other project participants.

### 1.2 Scope

The scope of this document is the University Library Management System Online (ULMS Online) project. The detailed capabilities and constraints should be confirmed against the approved project requirements.

### 1.3 Document Overview

The document presents stakeholders, functional requirements, non-functional requirements, use cases, and traceability information when these data are supplied.

## 2. Stakeholders

| ID | Name | Role | Type | Responsibilities | Needs |
| --- | --- | --- | --- | --- | --- |
| STK-01 | Ms. Hương | Head Librarian | University Central Library | Overall owner of library digital services | Overall owner of library digital services |
| STK-02 | Mr. Minh | IT Services Manager | University IT Department | Responsible for hosting, security and integration | Responsible for hosting, security and integration |
| STK-03 | Nguyễn Văn An | Student Representative | Student Union | Represents student self-service needs | Represents student self-service needs |

## 3. Functional Requirements

| ID | Title | Requirement Statement | Priority | Status | Acceptance Criteria |
| --- | --- | --- | --- | --- | --- |
| REQ-01 | Online member registration & login | The system shall allow students and staff to register an online account<br> linked to their university ID/email and log in securely via web browser. | Must | Approved | U; s; e; r;  ; c; a; n;  ; r; e; g; i; s; t; e; r;  ; w; i; t; h;  ; a;  ; v; a; l; i; d;  ; u; n; i; v; e; r; s; i; t; y;  ; e; m; a; i; l; /; I; D;  ; a; n; d;  ; s; u; c; c; e; s; s; f; u; l; l; y;  ; l; o; g;  ; i; n; ;;  ; a;  ; s; e; c; u; r; e;  ; s; e; s; s; i; o; n;  ; i; s;  ; e; s; t; a; b; l; i; s; h; e; d; . |
| REQ-02 | Online catalogue search | The system shall allow any authenticated or guest user to search<br> the book catalogue by title, author, ISBN, subject or year via <br>the web interface. | Must | Approved | S; e; a; r; c; h;  ; r; e; t; u; r; n; s;  ; r; e; l; e; v; a; n; t;  ; r; e; s; u; l; t; s;  ; w; i; t; h;  ; a; v; a; i; l; a; b; i; l; i; t; y;  ; s; t; a; t; u; s;  ; w; i; t; h; i; n;  ; t; h; e;  ; t; a; r; g; e; t;  ; r; e; s; p; o; n; s; e;  ; t; i; m; e; . |
| REQ-03 | Online digital access request | The system shall allow a logged-in member to request digital access (loan) for an available book online. The system shall record the request and make it available for the Admin to review and approve or reject. | Must | Approved | A;  ; m; e; m; b; e; r;  ; c; a; n;  ; s; u; b; m; i; t;  ; a; n;  ; a; c; c; e; s; s;  ; r; e; q; u; e; s; t; ;;  ; t; h; e;  ; s; y; s; t; e; m;  ; r; e; c; o; r; d; s;  ; i; t; s;  ; s; t; a; t; u; s;  ; a; s;  ; P; e; n; d; i; n; g;  ; A; p; p; r; o; v; a; l; ;;  ; a; n;  ; A; d; m; i; n;  ; c; a; n;  ; a; p; p; r; o; v; e;  ; o; r;  ; r; e; j; e; c; t;  ; i; t; ,;  ; a; n; d;  ; t; h; e;  ; m; e; m; b; e; r;  ; c; a; n;  ; s; e; e;  ; t; h; e;  ; u; p; d; a; t; e; d;  ; s; t; a; t; u; s; . |
| REQ-04 | Digital Copyright Violation and Fine Management | The system shall record and manage suspected copyright violations involving digital books, including unauthorized copying, downloading, sharing, redistribution, and attempts to bypass copyright protection mechanisms. An authorized Admin shall review reported violations and confirm whether a violation has occurred before issuing a fine. The fine amount shall be determined by the confirmed severity level: Level 1 — 10,000 VND, Level 2 — 20,000 VND, and Level 3 — 50,000 VND. The system shall record the violation details, confirmed severity level, fine amount, and payment status, and allow the affected User to view the fine and make a simulated payment | Should | Approved | T; h; e;  ; s; y; s; t; e; m;  ; r; e; c; o; r; d; s;  ; s; u; s; p; e; c; t; e; d;  ; c; o; p; y; r; i; g; h; t;  ; v; i; o; l; a; t; i; o; n; s;  ; i; n; v; o; l; v; i; n; g;  ; u; n; a; u; t; h; o; r; i; z; e; d;  ; c; o; p; y; i; n; g; ,;  ; d; o; w; n; l; o; a; d; i; n; g; ,;  ; s; h; a; r; i; n; g; ,;  ; r; e; d; i; s; t; r; i; b; u; t; i; o; n; ,;  ; o; r;  ; a; t; t; e; m; p; t; s;  ; t; o;  ; b; y; p; a; s; s;  ; c; o; p; y; r; i; g; h; t;  ; p; r; o; t; e; c; t; i; o; n;  ; m; e; c; h; a; n; i; s; m; s; .;  ; A; n;  ; a; u; t; h; o; r; i; z; e; d;  ; A; d; m; i; n;  ; c; a; n;  ; r; e; v; i; e; w;  ; a;  ; r; e; p; o; r; t; e; d;  ; v; i; o; l; a; t; i; o; n;  ; a; n; d;  ; c; o; n; f; i; r; m;  ; o; r;  ; r; e; j; e; c; t;  ; i; t; .;  ; A;  ; f; i; n; e;  ; i; s;  ; i; s; s; u; e; d;  ; o; n; l; y;  ; a; f; t; e; r;  ; t; h; e;  ; A; d; m; i; n;  ; c; o; n; f; i; r; m; s;  ; a;  ; v; i; o; l; a; t; i; o; n; .;  ; T; h; e;  ; f; i; n; e;  ; a; m; o; u; n; t;  ; m; a; t; c; h; e; s;  ; t; h; e;  ; c; o; n; f; i; r; m; e; d;  ; s; e; v; e; r; i; t; y;  ; l; e; v; e; l; :;  ; L; e; v; e; l;  ; 1;  ; —;  ; 1; 0; ,; 0; 0; 0;  ; V; N; D; ,;  ; L; e; v; e; l;  ; 2;  ; —;  ; 2; 0; ,; 0; 0; 0;  ; V; N; D; ,;  ; a; n; d;  ; L; e; v; e; l;  ; 3;  ; —;  ; 5; 0; ,; 0; 0; 0;  ; V; N; D; .;  ; T; h; e;  ; s; y; s; t; e; m;  ; r; e; c; o; r; d; s;  ; t; h; e;  ; f; i; n; e;  ; a; n; d;  ; p; a; y; m; e; n; t;  ; s; t; a; t; u; s; ,;  ; a; l; l; o; w; s;  ; t; h; e;  ; a; f; f; e; c; t; e; d;  ; U; s; e; r;  ; t; o;  ; v; i; e; w;  ; t; h; e;  ; f; i; n; e; ,;  ; a; n; d;  ; s; u; p; p; o; r; t; s;  ; s; i; m; u; l; a; t; e; d;  ; p; a; y; m; e; n; t; .;  ; D; i; g; i; t; a; l;  ; l; o; a; n;  ; e; x; p; i; r; y;  ; a; n; d;  ; r; e; a; d; i; n; g;  ; a; c; c; e; s; s;  ; r; e; v; o; c; a; t; i; o; n;  ; a; r; e;  ; v; e; r; i; f; i; e; d;  ; s; e; p; a; r; a; t; e; l; y;  ; a; g; a; i; n; s; t;  ; R; E; Q; -; 1; 2; . |
| REQ-05 | Audit log for authentication and administrative security actions | The system shall record authentication and administrative security events, including successful and failed login attempts, digital access request decisions, loan renewals, and the application or removal of account sanctions. Each record shall include the actor or system source, timestamp, event type, target account or request where applicable, outcome, and relevant details. | Must | Approved | E; a; c; h;  ; t; e; s; t; e; d;  ; a; u; t; h; e; n; t; i; c; a; t; i; o; n; ,;  ; a; c; c; e; s; s; -; r; e; q; u; e; s; t;  ; d; e; c; i; s; i; o; n; ,;  ; r; e; n; e; w; a; l; ,;  ; a; n; d;  ; s; a; n; c; t; i; o; n;  ; a; c; t; i; o; n;  ; h; a; s;  ; a;  ; c; o; r; r; e; s; p; o; n; d; i; n; g;  ; a; c; c; u; r; a; t; e;  ; a; u; d; i; t;  ; r; e; c; o; r; d;  ; w; i; t; h;  ; a; c; t; o; r;  ; s; y; s; t; e; m;  ; s; o; u; r; c; e; ,;  ; t; i; m; e; s; t; a; m; p; ,;  ; e; v; e; n; t;  ; t; y; p; e; ,;  ; o; u; t; c; o; m; e; ,;  ; a; n; d;  ; r; e; l; e; v; a; n; t;  ; d; e; t; a; i; l; s; ;;  ; u; n; a; u; t; h; o; r; i; z; e; d;  ; U; s; e; r; s;  ; c; a; n; n; o; t;  ; v; i; e; w;  ; a; u; d; i; t;  ; r; e; c; o; r; d; s; . |
| REQ-06 | Role-based access control (Web) | The system shall enforce role-based access control so that Users and Admins can only view and perform actions permitted for their roles. | Must | Approved | A;  ; U; s; e; r;  ; a; c; c; o; u; n; t;  ; c; a; n; n; o; t;  ; a; c; c; e; s; s;  ; A; d; m; i; n; -; o; n; l; y;  ; p; a; g; e; s;  ; o; r;  ; f; u; n; c; t; i; o; n; s; ;;  ; a; n;  ; A; d; m; i; n;  ; c; a; n;  ; a; c; c; e; s; s;  ; a; u; t; h; o; r; i; z; e; d;  ; a; d; m; i; n; i; s; t; r; a; t; i; o; n;  ; f; u; n; c; t; i; o; n; s; . |
| REQ-07 | Online loan renewal | The system shall allow eligible members to renew their digital loans online (subject to reservation queue and maximum renewal limit). | Should | Approved | M; e; m; b; e; r;  ; c; a; n;  ; r; e; n; e; w;  ; a; n;  ; e; l; i; g; i; b; l; e;  ; l; o; a; n; ;;  ; n; e; w;  ; d; u; e;  ; d; a; t; e;  ; i; s;  ; u; p; d; a; t; e; d;  ; a; n; d;  ; c; o; n; f; i; r; m; e; d; . |
| REQ-08 | Online loan history & fine view | The system shall allow a logged-in member to view current digital loans, borrowing history, due dates and outstanding fines through the web portal. | Should | Approved | M; e; m; b; e; r;  ; c; a; n;  ; v; i; e; w;  ; c; u; r; r; e; n; t;  ; l; o; a; n; s; ,;  ; p; a; s; t;  ; l; o; a; n; s;  ; a; n; d;  ; o; u; t; s; t; a; n; d; i; n; g;  ; f; i; n; e; s;  ; w; i; t; h;  ; a; c; c; u; r; a; t; e;  ; s; t; a; t; u; s;  ; a; n; d;  ; d; a; t; e; s; . |
| REQ-09 | Add books to favourites list | The system shall allow a logged-in User to add or remove books from a personal favourites list and view that list later. | Should | Proposed | A;  ; U; s; e; r;  ; c; a; n;  ; a; d; d;  ; a;  ; b; o; o; k;  ; t; o;  ; f; a; v; o; u; r; i; t; e; s; ,;  ; s; e; e;  ; i; t;  ; i; n;  ; t; h; e; i; r;  ; l; i; s; t; ,;  ; a; n; d;  ; r; e; m; o; v; e;  ; i; t;  ; f; r; o; m;  ; t; h; e;  ; l; i; s; t; . |
| REQ-10 | Read books online | The system shall allow a User with valid digital access to read the selected book online through the web interface. | Must | Proposed | A;  ; U; s; e; r;  ; w; i; t; h;  ; a; p; p; r; o; v; e; d; ,;  ; u; n; e; x; p; i; r; e; d;  ; a; c; c; e; s; s;  ; c; a; n;  ; o; p; e; n;  ; a; n; d;  ; r; e; a; d;  ; t; h; e;  ; b; o; o; k;  ; o; n; l; i; n; e; ;;  ; a;  ; U; s; e; r;  ; w; i; t; h; o; u; t;  ; v; a; l; i; d;  ; a; c; c; e; s; s;  ; i; s;  ; d; e; n; i; e; d; . |
| REQ-11 | Request to borrow a book again | The system shall allow a logged-in User to submit a new digital access request for a book they have borrowed previously, subject to availability and account restrictions. | Should | Proposed | A;  ; U; s; e; r;  ; c; a; n;  ; r; e; q; u; e; s; t;  ; a; c; c; e; s; s;  ; a; g; a; i; n; ;;  ; t; h; e;  ; s; y; s; t; e; m;  ; c; h; e; c; k; s;  ; a; v; a; i; l; a; b; i; l; i; t; y;  ; a; n; d;  ; a; c; c; o; u; n; t;  ; r; e; s; t; r; i; c; t; i; o; n; s;  ; a; n; d;  ; d; i; s; p; l; a; y; s;  ; t; h; e;  ; r; e; q; u; e; s; t;  ; s; t; a; t; u; s; . |
| REQ-12 | Automatically revoke reading access at expiry | The system shall verify digital loan expiry whenever a User attempts to access a digital book. If the loan has expired, the system shall revoke the active reading permission, record the expiry event, and deny further access. | Must | Proposed | A; t;  ; t; h; e;  ; a; p; p; r; o; v; e; d;  ; l; o; a; n;  ; e; x; p; i; r; y;  ; t; i; m; e; ,;  ; t; h; e;  ; U; s; e; r;  ; c; a; n;  ; n; o;  ; l; o; n; g; e; r;  ; o; p; e; n;  ; o; r;  ; c; o; n; t; i; n; u; e;  ; a; c; c; e; s; s; i; n; g;  ; t; h; e;  ; b; o; o; k; .;  ; T; h; e;  ; s; y; s; t; e; m;  ; r; e; c; o; r; d; s;  ; t; h; e;  ; e; x; p; i; r; e; d;  ; a; c; c; e; s; s;  ; s; t; a; t; u; s;  ; w; i; t; h; o; u; t;  ; r; e; q; u; i; r; i; n; g;  ; t; h; e;  ; U; s; e; r;  ; t; o;  ; r; e; o; p; e; n;  ; t; h; e;  ; b; o; o; k;  ; o; r;  ; a; n;  ; A; d; m; i; n;  ; t; o;  ; t; a; k; e;  ; m; a; n; u; a; l;  ; a; c; t; i; o; n; . |
| REQ-13 | Manage account violations and sanctions | The system shall apply sanctions according to the library rules configured by an authorized administrator. | Must | Proposed | T; h; e;  ; A; d; m; i; n;  ; r; e; c; e; i; v; e; s;  ; a; n;  ; a; l; e; r; t;  ; f; o; r;  ; a;  ; c; o; n; f; i; g; u; r; e; d;  ; v; i; o; l; a; t; i; o; n;  ; c; o; n; d; i; t; i; o; n; ,;  ; c; a; n;  ; r; e; v; i; e; w;  ; i; t;  ; a; n; d;  ; a; p; p; l; y;  ; o; r;  ; r; e; m; o; v; e;  ; a; c; c; o; u; n; t;  ; r; e; s; t; r; i; c; t; i; o; n; s; ;;  ; e; a; c; h;  ; a; c; t; i; o; n; ,;  ; r; e; a; s; o; n;  ; a; n; d;  ; t; i; m; e; s; t; a; m; p;  ; i; s;  ; r; e; c; o; r; d; e; d; . |
| REQ-14 | Loan Expiration Notification and Automatic Reading Access Revocatio | The system shall notify the User one day before the loan period expires. When the loan period expires, the system shall automatically revoke the User's reading access to the corresponding digital book. After access is revoked, the User shall not be able to open or continue reading the book unless the User submits a new borrowing request and the request is approved. The system shall not send overdue notifications. | Should | Proposed | 1; .;  ; T; h; e;  ; n; e; x; t;  ; e; l; i; g; i; b; l; e;  ; U; s; e; r;  ; r; e; c; e; i; v; e; s;  ; a;  ; n; o; t; i; f; i; c; a; t; i; o; n;  ; w; h; e; n;  ; a;  ; r; e; s; e; r; v; e; d;  ; d; i; g; i; t; a; l;  ; c; o; p; y;  ; b; e; c; o; m; e; s;  ; a; v; a; i; l; a; b; l; e; .;  ; 2; .;  ; T; h; e;  ; s; y; s; t; e; m;  ; a; u; t; o; m; a; t; i; c; a; l; l; y;  ; r; e; v; o; k; e; s;  ; t; h; e;  ; U; s; e; r; '; s;  ; r; e; a; d; i; n; g;  ; a; c; c; e; s; s;  ; t; o;  ; t; h; e;  ; c; o; r; r; e; s; p; o; n; d; i; n; g;  ; d; i; g; i; t; a; l;  ; b; o; o; k;  ; w; h; e; n;  ; t; h; e;  ; l; o; a; n;  ; p; e; r; i; o; d;  ; e; x; p; i; r; e; s; .;  ; 3; .;  ; N; o;  ; o; v; e; r; d; u; e;  ; n; o; t; i; f; i; c; a; t; i; o; n;  ; i; s;  ; s; e; n; t;  ; w; h; e; n;  ; a;  ; l; o; a; n;  ; b; e; c; o; m; e; s;  ; o; v; e; r; d; u; e; .;  ; 4; .;  ; N; o;  ; u; n; r; e; l; a; t; e; d;  ; U; s; e; r;  ; i; s;  ; n; o; t; i; f; i; e; d; . |
| REQ-15 | Secure input validation against injection attack | The system shall validate and safely process User-provided input to prevent SQL injection and cross-site scripting (XSS). Input shall not be executed as SQL commands or browser scripts. | Must | Proposed | S; Q; L;  ; i; n; j; e; c; t; i; o; n;  ; t; e; s; t;  ; i; n; p; u; t;  ; d; o; e; s;  ; n; o; t;  ; c; a; u; s; e;  ; u; n; a; u; t; h; o; r; i; z; e; d;  ; d; a; t; a;  ; c; h; a; n; g; e; s; ;;  ; X; S; S;  ; t; e; s; t;  ; i; n; p; u; t;  ; d; o; e; s;  ; n; o; t;  ; e; x; e; c; u; t; e;  ; s; c; r; i; p; t; s;  ; i; n;  ; t; h; e;  ; b; r; o; w; s; e; r; . |
| REQ-16 | Audit log for reservation, return, and fine transactions | The system shall record circulation and financial transactions, including placing or cancelling a digital reservation, processing a return or closing a loan, and creating or adjusting a fine. Each record shall include the actor or system source, timestamp, transaction type, related book/loan/reservation/member, and relevant transaction details. | Must | Proposed | E; v; e; r; y;  ; t; e; s; t; e; d;  ; r; e; s; e; r; v; a; t; i; o; n; ,;  ; r; e; s; e; r; v; a; t; i; o; n;  ; c; a; n; c; e; l; l; a; t; i; o; n; ,;  ; r; e; t; u; r; n; /; l; o; a; n;  ; c; l; o; s; u; r; e; ,;  ; a; n; d;  ; f; i; n; e;  ; c; r; e; a; t; i; o; n;  ; o; r;  ; a; d; j; u; s; t; m; e; n; t;  ; h; a; s;  ; a;  ; c; o; r; r; e; s; p; o; n; d; i; n; g;  ; a; c; c; u; r; a; t; e;  ; a; u; d; i; t;  ; r; e; c; o; r; d;  ; c; o; n; t; a; i; n; i; n; g;  ; t; h; e;  ; a; c; t; o; r; /; s; y; s; t; e; m;  ; s; o; u; r; c; e; ,;  ; t; i; m; e; s; t; a; m; p; ,;  ; t; r; a; n; s; a; c; t; i; o; n;  ; t; y; p; e; ,;  ; r; e; l; a; t; e; d;  ; r; e; c; o; r; d; ,;  ; a; n; d;  ; r; e; l; e; v; a; n; t;  ; d; e; t; a; i; l; s; ;;  ; n; o;  ; p; e; r; f; o; r; m; e; d;  ; t; r; a; n; s; a; c; t; i; o; n;  ; i; s;  ; m; i; s; s; i; n; g; . |
| REQ-17 | Approval of digital access requests by Admin | The system shall allow an authenticated Admin to approve or reject a valid pending digital access request. Upon approval, the system shall update the request status and grant online reading access according to the borrowing rules. The decision shall be recorded. | Must | Proposed | T; h; e;  ; A; d; m; i; n;  ; c; a; n;  ; a; p; p; r; o; v; e;  ; a;  ; v; a; l; i; d;  ; p; e; n; d; i; n; g;  ; r; e; q; u; e; s; t; ;;  ; i; t; s;  ; s; t; a; t; u; s;  ; c; h; a; n; g; e; s;  ; t; o;  ; A; p; p; r; o; v; e; d; ;;  ; t; h; e;  ; U; s; e; r;  ; c; a; n;  ; r; e; a; d;  ; t; h; e;  ; b; o; o; k;  ; a; c; c; o; r; d; i; n; g;  ; t; o;  ; t; h; e;  ; a; c; c; e; s; s;  ; r; u; l; e; s; ;;  ; a; n; d;  ; t; h; e;  ; d; e; c; i; s; i; o; n;  ; i; s;  ; r; e; c; o; r; d; e; d; . |

## 4. Non-Functional Requirements

| ID | Title | Category | Requirement Statement | Priority | Metric | Target | Unit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NFR-01 | Web search response time | Performance | The system shall return catalogue search results within the specified response-time target under normal concurrent load. | Must | 95th percentile catalogue search response time | <= 2 seconds |  |
| NFR-02 | System availability | Availability | The system shall maintain the specified service availability during the defined operating period. | Must | Monthly availability | ≥ 99.5% per month |  |
| NFR-03 | Usability (web interface) | Usability | New users shall be able to complete core tasks (search, reserve, renew) without training. | Should | task success rate for first-time users | >= 90% success on first attempt |  |
| NFR-04 | Data protection & session security | Security | The system shall protect authenticated sessions and sensitive user data against unauthorized access. | Must | encryption & session policy | All defined security test cases for session protection and sensitive-data access shall pass. |  |
| NFR-05 | Scalability & concurrency | Scalability | The system shall support concurrent access by at least 300 users while maintaining the defined performance and error-rate limits. | Could | Number of concurrent users; 95th percentile response time; request error rate | At least 300 concurrent users; catalogue search response time ≤ 2 seconds at the 95th percentile; request error rate < 1% during the defined load test |  |
| NFR-06 | Data integrity | Reliability | The system shall maintain consistent loan, reservation, fine and digital-access records when transactions are completed. | Must | Number of inconsistent records after completed transactions | Zero inconsistent records in the defined transaction-integrity test suite |  |
| NFR-07 | Browser compatibility | Compatibility | The system shall provide its core functionality through supported modern web browsers. Core workflows, including authentication, catalogue search, digital access requests, and loan management, shall operate consistently across the browsers included in the project's supported-browser list. | Should | Core workflow compatibility | 100% of defined core workflow tests pass on each supported browser. |  |
| NFR-08 | Backup and recovery | Reliability | The system shall support data backup and recovery procedures to protect stored information against data loss caused by system failures or other incidents. Backup frequency, retention periods, and recovery objectives shall be defined according to the project's operational requirements. | Must | Backup frequency and recovery time | Critical data shall be backed up at least once every 24 hours. Restoration of the defined recovery test dataset shall be completed within 4 hours after recovery begins. |  |
| NFR-09 | Web accessibility | Accessibility | The system's web interface shall be designed to support accessibility for users with different abilities and assistive technologies. The interface shall target WCAG 2.2 Level AA conformance, including appropriate keyboard accessibility, form labels, text alternatives for meaningful images, and sufficient color contrast. | Should | WCAG 2.2 Level AA conformance | Meet applicable WCAG 2.2 Level AA success criteria for the defined core user workflows. |  |
| NFR-10 | Digital rights management and unauthorized download protection | Security | The system shall restrict access to digital book content to authenticated users with valid reading permissions. Protected book files shall not be directly accessible through public URLs, and access shall be denied when reading permission expires or is revoked. | Must | Unauthorized access prevention | 100% of defined unauthorized-access test cases are rejected, including unauthenticated access, expired or revoked permissions, and suspended or banned accounts. |  |

## 5. Use Cases

### UC-01: Register / Log in to Web Portal

**Description:** Create an account or authenticate securely to access online library services.
**Primary Actor:** User
**Priority:** 
**Status:** 

**Preconditions:**

- For registration, the person has a valid university email or student/staff ID and no existing account; for login, an account exists and is not suspended.

**Main Flow:**

User opens the web portal
User selects Register or Login
For registration, User enters the required details
For login, User enters credentials
System validates the submitted information
System creates the account or establishes an authenticated session
System displays the member dashboard.

**Alternative Flows:**

- Registration details are invalid or the account already exists – system displays an explanation
- Login credentials are invalid – system displays an error and allows retry
- Suspended account – system denies access and displays an appropriate message.

**Postconditions:**

- A valid account is created or the member is authenticated; invalid or restricted attempts do not create an authenticated session.

---

### UC-02: Search Online Catalogue

**Description:** Find books and research materials in the university library catalogue through the web interface.
**Primary Actor:** User
**Priority:** 
**Status:** 

**Preconditions:**

- The online catalogue is available; browsing and searching are available to guests or authenticated users.

**Main Flow:**

User opens the catalogue
User enters keywords or selects search filters such as title, author, ISBN, subject, or year
System validates the search input
System searches the catalogue
System displays matching records and their availability or digital-access status
User may open a book record for more details.

**Alternative Flows:**

- No matching records – system displays a no-results message and may suggest changing search terms
- Invalid or empty search input – system prompts the User to enter valid criteria.

**Postconditions:**

- Search results or an informative no-results message are displayed; catalogue data is not modified.

---

### UC-03: Request Digital Access to a Book

**Description:** Submit a request for digital access to a book and track its approval status.
**Primary Actor:** User
**Priority:** 
**Status:** 

**Preconditions:**

- User is logged in; the selected book exists; the account satisfies configured eligibility rules.

**Main Flow:**

User searches for and opens a book record
User selects Request Access
System checks the user's eligibility and the book's access conditions
System creates a digital access request with Pending Approval status
System adds the request to the pending access-request list
System displays a confirmation message and the request status to the User.

**Alternative Flows:**

- User is not authenticated: system prompts the User to log in
- User is ineligible: system rejects the request and explains the reason
- A duplicate pending request exists: system informs the User and does not create another request
- The book does not support digital access requests: system informs the User that the request cannot be submitted.

**Postconditions:**

- A valid access request is recorded with Pending Approval status and is available for Admin review; otherwise, no duplicate or invalid request is created.

---

### UC-04: Renew Digital Loan Online

**Description:** Extend an eligible digital loan online according to library renewal rules.
**Primary Actor:** User
**Priority:** 
**Status:** 

**Preconditions:**

- User is logged in and has an active digital loan; the loan satisfies the configured renewal rules, including reservation-queue and maximum-renewal limits.

**Main Flow:**

User opens My Loans
User selects an eligible loan and chooses Renew
System checks the loan status, reservation queue, and renewal limit
System calculates the new expiry date according to the configured renewal rules
System updates the loan record
System displays the new expiry date and confirms the renewal.

**Alternative Flows:**

- The loan has expired: system rejects the renewal and explains why
- Another member is waiting in the reservation queue: system rejects the renewal according to the reservation rules
- The maximum renewal limit has been reached: system rejects the renewal
- A system error occurs: system retains the original loan record and displays an error message.

**Postconditions:**

- If renewal succeeds, the loan expiry date is updated; otherwise, the original loan record remains unchanged.

---

### UC-05: Manage Digital Loan Expiry and Access Revocation

**Description:** Ensure that digital reading access is revoked when the approved loan period expires.
**Primary Actor:** System
**Priority:** 
**Status:** 

**Preconditions:**

- The User has an existing digital loan.The digital loan has an expiry date.The system can verify the loan status and the User's reading permissions.

**Main Flow:**

The system checks the digital loan's expiry date and status.The system determines whether the loan has expired or is no longer valid.If the loan remains valid, the system keeps reading access available according to the loan permissions.If the loan has expired or is no longer valid, the system revokes the User's reading access.The system records the relevant expiry or access-revocation event.If the User attempts to open the expired or revoked book, the system denies access to the protected digital book content.

**Alternative Flows:**

- Loan has not expired: The system keeps reading access active while the loan remains valid.
Loan has been renewed: The system uses the updated expiry date and keeps access available if the renewed loan is valid.
Access revocation fails: The system records the failure for further investigation and does not silently treat the revocation as successful.
User accesses an expired loan: The system denies access to the protected digital book content.

**Postconditions:**

- Expired or invalid loans no longer provide reading access.
Valid loans retain access according to their permissions.
The system records the relevant expiry or access-revocation event.

---

### UC-06: View Loans, Borrowing History and Fines

**Description:** View the member's own current loans, past loans, expiry dates, and outstanding fines online.
**Primary Actor:** User
**Priority:** 
**Status:** 

**Preconditions:**

- User is logged in.

**Main Flow:**

User opens My Loans or My Account
System retrieves records belonging to the authenticated User
System displays current loans, borrowing history, expiry/due dates, and fine status
User reviews the displayed information.

**Alternative Flows:**

- No loan history exists – system displays an empty-state message
- No fine is outstanding – system displays a zero or no-outstanding-fines status
- Records cannot be retrieved – system displays an error without exposing another member's data.

**Postconditions:**

- The User sees only their own loan and fine information; no records are modified.

---

### UC-07: Read Digital Books Online

**Description:** Read a selected digital book through the web interface while valid access is granted.
**Primary Actor:** User
**Priority:** 
**Status:** 

**Preconditions:**

- User is logged in and has approved, unexpired access to the selected book; the digital content is available.

**Main Flow:**

User opens My Loans or the relevant book record
User selects Read Online
System verifies the user's account status and current access permission
System opens the online reader
User reads and navigates the available content while access remains valid.

**Alternative Flows:**

- No approved loan exists, access has expired, or the account is suspended – system denies access and displays an appropriate message
- Digital content is temporarily unavailable – system displays an error without exposing protected content.

**Postconditions:**

- Authorized User can read the book while permission remains valid; unauthorized access is denied.

---

### UC-08: Review and Decide Digital Access Requests

**Description:** Review pending digital access requests and approve or reject each request according to library rules.
**Primary Actor:** Admin
**Priority:** 
**Status:** 

**Preconditions:**

- Admin is authenticated with the required role; at least one pending digital access request exists.

**Main Flow:**

Admin opens the pending access-request list
System displays pending requests
Admin selects a request
System displays the request, member, and book details
Admin reviews the request and selects Approve or Reject
Admin records a reason when required by library policy
System validates that the request is still pending and that the decision is permitted
System updates the request status
If approved, system grants reading access according to the configured access rules
System makes the decision visible to the member
System records the decision, administrator, and timestamp in the audit log.

**Alternative Flows:**

- The request is no longer pending: system refreshes the request status and prevents a conflicting decision
- The member or book is no longer eligible: system prevents approval and displays the reason
- Admin lacks permission: system denies the action
- The status update fails: system reports the failure and does not display a false success confirmation.

**Postconditions:**

- The request has an updated decision status. An approved request receives reading access according to the configured rules; a rejected request does not receive access from that request. The decision is recorded for audit.

---

### UC-09: Manage Favourite Books

**Description:** Maintain a personal list of favourite books for later reference.
**Primary Actor:** User
**Priority:** 
**Status:** 

**Preconditions:**

- User is logged in and the selected book exists in the catalogue.

**Main Flow:**

User opens a book record
User selects Add to Favourites
System adds the book to the authenticated User's favourites list
User opens the favourites list
System displays the saved books
User may open a saved book or remove it from the list
System updates the favourites list after a successful removal.

**Alternative Flows:**

- The book is already a favourite: system informs the User and does not create a duplicate entry
- The book has been removed from the catalogue: system handles the unavailable record without causing an error
- An update fails: system informs the User and preserves the previous favourites list.

**Postconditions:**

- The favourites list reflects the latest successful action and remains associated with the authenticated User.

---

### UC-10: Request Access Again to a Previously Borrowed Book

**Description:** Submit a new digital access request for a book the member has borrowed before.
**Primary Actor:** User
**Priority:** 
**Status:** 

**Preconditions:**

- User is logged in; the book appears in the User's borrowing history; the account and book satisfy the current access rules.

**Main Flow:**

User opens borrowing history
User selects a previously borrowed book
User chooses Request Access Again
System checks the User's eligibility and the book's access conditions
System checks whether a pending request already exists
System creates a new digital access request with Pending Approval status
System adds the request to the pending access-request list
System displays confirmation and the request status to the User.

**Alternative Flows:**

- User is not logged in: The system prompts the User to log in before accessing borrowing history or submitting an access request.
The book is unavailable: The system rejects the request and informs the User that the book is currently unavailable.
The User is not eligible: The system rejects the request and displays the reason. No new access request is created.
A pending request already exists: The system prevents the creation of a duplicate request and informs the User that an access request for the same book is already pending.

**Postconditions:**

- A valid new access request is recorded with Pending Approval status, or the User is informed why the request cannot be submitted.

---

### UC-11: Manage Account Violations and Sanctions

**Description:** Review account-violation alerts and apply or remove account restrictions with an audit trail.
**Primary Actor:** Admin
**Priority:** 
**Status:** 

**Preconditions:**

- Admin is authenticated with the required role; a configured violation alert or account case exists.

**Main Flow:**

Admin opens the violation alerts or account-management page
Admin reviews the account and violation details
Admin selects an allowed action such as suspend, ban, or restore/unban
Admin records a reason
System updates account restrictions and related reading permissions
System records the action, reason, actor, and timestamp in the audit log.

**Alternative Flows:**

- No violation alert exists – system displays an empty state
- Admin lacks permission – system denies the action
- Action cannot be completed – system reports the failure and retains the previous account status.

**Postconditions:**

- The account status reflects the authorized action; reading access follows the restriction; the action is auditable.

---

### UC-12: Reserve an Unavailable Digital Book

**Description:** Reserve a digital book when no digital copies are currently available.
**Primary Actor:** User
**Priority:** 
**Status:** 

**Preconditions:**

- User is logged in; the selected book exists; no digital copies are currently available; the User satisfies the reservation rules.

**Main Flow:**

User opens the book record
System displays that no digital copies are currently available
User selects Reserve
System checks the User's eligibility and existing reservations
System adds the User to the reservation queue
System records the reservation and queue position
System displays the reservation confirmation and status.

**Alternative Flows:**

- User opens the book record
- System displays that no digital copies are currently available
- User selects Reserve
- System checks the User's eligibility and existing reservations
- System adds the User to the reservation queue
- System records the reservation and queue position
- System displays the reservation confirmation and status.

**Postconditions:**

- A valid reservation is recorded in the queue, and reading access is not granted until the configured availability and access conditions are satisfied.

---

### UC-13: Receive Library Notifications

**Description:** Receive notifications about reservation availability and overdue loans.
**Primary Actor:** User
**Priority:** 
**Status:** 

**Preconditions:**

- A relevant reservation or overdue-loan event has occurred; the User's notification details and notification settings satisfy the configured rules.

**Main Flow:**

System detects a reservation-availability or overdue-loan event
System identifies the affected User
System prepares a notification containing the relevant information
System sends the notification through the configured channel
System records the notification attempt and its result.

**Alternative Flows:**

- No eligible User is identified: system does not send the notification and records the result where required
- Notification delivery fails: system records the failure and retries according to the configured policy
- The event is no longer relevant: system does not send an outdated notification.

**Postconditions:**

- The notification is sent or its delivery failure is recorded.

---

## 6. Requirements Traceability

| Source ID | Target ID | Relationship | Description |
| --- | --- | --- | --- |
| REQ-01 | UC-01 | Requirement -> Use Case | Related to use case: Register / Log in to Web Portal |
| REQ-06 | UC-01 | Requirement -> Use Case | Related to use case: Register / Log in to Web Portal |
| REQ-02 | UC-02 | Requirement -> Use Case | Related to use case: Search Online Catalogue |
| REQ-03 | UC-03 | Requirement -> Use Case | Related to use case: Request Digital Access to a Book |
| REQ-06 | UC-03 | Requirement -> Use Case | Related to use case: Request Digital Access to a Book |
| REQ-07 | UC-04 | Requirement -> Use Case | Related to use case: Renew Digital Loan Online |
| REQ-06 | UC-04 | Requirement -> Use Case | Related to use case: Renew Digital Loan Online |
| REQ-12 | UC-05 | Requirement -> Use Case | Related to use case: Manage Digital Loan Expiry and Access Revocation |
| REQ-08 | UC-06 | Requirement -> Use Case | Related to use case: View Loans, Borrowing History and Fines |
| REQ-04 | UC-06 | Requirement -> Use Case | Related to use case: View Loans, Borrowing History and Fines |
| REQ-10 | UC-07 | Requirement -> Use Case | Related to use case: Read Digital Books Online |
| REQ-12 | UC-07 | Requirement -> Use Case | Related to use case: Read Digital Books Online |
| REQ-06 | UC-07 | Requirement -> Use Case | Related to use case: Read Digital Books Online |
| REQ-03 | UC-08 | Requirement -> Use Case | Related to use case: Review and Decide Digital Access Requests |
| REQ-05 | UC-08 | Requirement -> Use Case | Related to use case: Review and Decide Digital Access Requests |
| REQ-06 | UC-08 | Requirement -> Use Case | Related to use case: Review and Decide Digital Access Requests |
| REQ-09 | UC-09 | Requirement -> Use Case | Related to use case: Manage Favourite Books |
| REQ-11 | UC-10 | Requirement -> Use Case | Related to use case: Request Access Again to a Previously Borrowed Book |
| REQ-03 | UC-10 | Requirement -> Use Case | Related to use case: Request Access Again to a Previously Borrowed Book |
| REQ-06 | UC-10 | Requirement -> Use Case | Related to use case: Request Access Again to a Previously Borrowed Book |
| REQ-13 | UC-11 | Requirement -> Use Case | Related to use case: Manage Account Violations and Sanctions |
| REQ-05 | UC-11 | Requirement -> Use Case | Related to use case: Manage Account Violations and Sanctions |
| REQ-06 | UC-11 | Requirement -> Use Case | Related to use case: Manage Account Violations and Sanctions |
| REQ-10 | UC-11 | Requirement -> Use Case | Related to use case: Manage Account Violations and Sanctions |
| REQ-05 | UC-12 | Requirement -> Use Case | Related to use case: Reserve an Unavailable Digital Book |
| REQ-06 | UC-12 | Requirement -> Use Case | Related to use case: Reserve an Unavailable Digital Book |
| REQ-15 | UC-13 | Requirement -> Use Case | Related to use case: Receive Library Notifications |
| REQ-01 | TC-01 | Requirement -> Test Case | Verified by test case: Register and log in with valid university credentials |
| REQ-02 | TC-02 | Requirement -> Test Case | Verified by test case: Catalogue search returns results within 2 seconds |
| REQ-03 | TC-03 | Requirement -> Test Case | Verified by test case: User submits a digital access request |
| REQ-07 | TC-04 | Requirement -> Test Case | Verified by test case: Eligible User renews a digital loan |
| REQ-06 | TC-05 | Requirement -> Test Case | Verified by test case: User cannot access Admin-only functions |
| REQ-10 | TC-06 | Requirement -> Test Case | Verified by test case: Expired digital access is revoked automatically |
| REQ-12 | TC-06 | Requirement -> Test Case | Verified by test case: Expired digital access is revoked automatically |
| REQ-08 | TC-07 | Requirement -> Test Case | Verified by test case: User views loan history and fines |
| REQ-04 | TC-07 | Requirement -> Test Case | Verified by test case: User views loan history and fines |
| REQ-05 | TC-08 | Requirement -> Test Case | Verified by test case: Audit log records authentication and access-control decisions |
| REQ-09 | TC-09 | Requirement -> Test Case | Verified by test case: User adds and removes a book from favourites |
| REQ-10 | TC-10 | Requirement -> Test Case | Verified by test case: User reads a book with valid approved access |
| REQ-12 | TC-10 | Requirement -> Test Case | Verified by test case: User reads a book with valid approved access |
| REQ-10 | TC-11 | Requirement -> Test Case | Verified by test case: User without valid access is denied online reading |
| REQ-12 | TC-11 | Requirement -> Test Case | Verified by test case: User without valid access is denied online reading |
| REQ-06 | TC-11 | Requirement -> Test Case | Verified by test case: User without valid access is denied online reading |
| REQ-11 | TC-12 | Requirement -> Test Case | Verified by test case: User requests access again to a previously borrowed book |
| REQ-03 | TC-12 | Requirement -> Test Case | Verified by test case: User requests access again to a previously borrowed book |
| REQ-11 | TC-13 | Requirement -> Test Case | Verified by test case: Repeat borrowing is blocked when book or account is ineligible |
| REQ-03 | TC-13 | Requirement -> Test Case | Verified by test case: Repeat borrowing is blocked when book or account is ineligible |
| REQ-06 | TC-13 | Requirement -> Test Case | Verified by test case: Repeat borrowing is blocked when book or account is ineligible |
| REQ-03 | TC-14 | Requirement -> Test Case | Verified by test case: Admin reviews an access request and approves or rejects it |
| REQ-05 | TC-14 | Requirement -> Test Case | Verified by test case: Admin reviews an access request and approves or rejects it |
| REQ-06 | TC-14 | Requirement -> Test Case | Verified by test case: Admin reviews an access request and approves or rejects it |
| REQ-13 | TC-15 | Requirement -> Test Case | Verified by test case: Admin applies and removes account sanctions |
| REQ-05 | TC-15 | Requirement -> Test Case | Verified by test case: Admin applies and removes account sanctions |
| REQ-06 | TC-15 | Requirement -> Test Case | Verified by test case: Admin applies and removes account sanctions |
| REQ-13 | TC-16 | Requirement -> Test Case | Verified by test case: Suspended or banned User cannot read digital books |
| REQ-10 | TC-16 | Requirement -> Test Case | Verified by test case: Suspended or banned User cannot read digital books |
| REQ-06 | TC-16 | Requirement -> Test Case | Verified by test case: Suspended or banned User cannot read digital books |
| REQ-04 | TC-17 | Requirement -> Test Case | Verified by test case: Copyright violation fine follows confirmed severity level |
| REQ-08 | TC-17 | Requirement -> Test Case | Verified by test case: Copyright violation fine follows confirmed severity level |
| REQ-05 | TC-18 | Requirement -> Test Case | Verified by test case: Audit log cannot be viewed by a normal User |
| REQ-06 | TC-18 | Requirement -> Test Case | Verified by test case: Audit log cannot be viewed by a normal User |
| REQ-05 | TC-19 | Requirement -> Test Case | Verified by test case: Member can reserve a book with no available digital copies |
| REQ-07 | TC-20 | Requirement -> Test Case | Verified by test case: Member is notified of successful renewal and updated expiry date |
| REQ-15 | TC-21 | Requirement -> Test Case | Verified by test case: Member is notified when their account is banned due to suspected copyright infringement |
| REQ-16 | TC-22 | Requirement -> Test Case | Verified by test case: Audit log records reservation, return, and fine transactions |
| REQ-15 | TC-23 | Requirement -> Test Case | Verified by test case: Web forms reject injection and safely encode script input |

## 7. Document Summary

| Artifact Type | Count |
|---|---:|
| Requirements | 17 |
| Non-Functional Requirements | 10 |
| Stakeholders | 3 |
| Use Cases | 13 |
| Traceability Links | 66 |

---

*End of document.*
