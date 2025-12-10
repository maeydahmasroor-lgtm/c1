# Feature Specification: Constitution Principles

**Feature Branch**: `001-constitution-principles`  
**Created**: 2025-12-10  
**Status**: Draft  
**Input**: User description: "### sp.specify → CONSTITUTION (final, short, unbreakable) 1. Answers come ONLY from the book’s own text. Anything else = “I don’t know”. 2. Selected/highlighted text is the highest authority. 3. No third-party widgets, trackers, analytics, or chat services. Ever. 4. OpenAI key never reaches the browser. 5. Must run forever on free tiers (Qdrant Free, Vercel Hobby, OpenAI pay-as-you-go). 6. Exactly one blue floating bubble (bottom-right). Nothing else floats. 7. Works on mobile and instantly follows Docusaurus dark mode. 8. Widget loads and opens even offline (just shows “no connection”). 9. Full deploy from zero in ≤ 60 minutes. 10. Remove the chatbot tomorrow → book still 100 % perfect. 10 rules. No exceptions. Ratified 10 Dec 2025.### sp.specify → CONSTITUTION (final, short, unbreakable) 1. Answers come ONLY from the book’s own text. Anything else = “I don’t know”. 2. Selected/highlighted text is the highest authority. 3. No third-party widgets, trackers, analytics, or chat services. Ever. 4. gemini key never reaches the browser. 5. Must run forever on free tiers (Qdrant Free). 6. Exactly one blue floating bubble (bottom-right). Nothing else floats. 7. Works on mobile and instantly follows Docusaurus dark mode. 8. Widget loads and opens even offline (just shows “no connection”)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Adherence to Content Origin (Priority: P1)

The system (agent/tool) provides responses strictly based on the book's text. If information is outside the book, the system acknowledges "I don't know".

**Why this priority**: Ensures authoritative and consistent information delivery.

**Independent Test**: Can be fully tested by querying for information both within and outside the book's content.

**Acceptance Scenarios**:

1.  **Given** a query whose answer is in the book, **When** the system responds, **Then** the answer is directly from the book's text.
2.  **Given** a query whose answer is not in the book, **When** the system responds, **Then** the system states "I don't know".

---

### User Story 2 - Prioritization of Highlighted Text (Priority: P1)

The system prioritizes selected or highlighted text as the most authoritative source for responses.

**Why this priority**: Ensures user-directed focus and accuracy.

**Independent Test**: Can be fully tested by providing queries with both general text and selected/highlighted text.

**Acceptance Scenarios**:

1.  **Given** a query with both general and selected/highlighted text, **When** the system responds, **Then** the response reflects the selected/highlighted text as the primary source.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: System MUST provide answers ONLY from the book’s own text.
-   **FR-002**: System MUST respond "I don't know" if the answer is not in the book's text.
-   **FR-003**: System MUST treat selected/highlighted text as the highest authority.
-   **FR-004**: System MUST NOT include any third-party widgets, trackers, analytics, or chat services.
-   **FR-005**: System MUST ensure the gemini key never reaches the browser.
-   **FR-006**: System MUST run forever on free tiers (Qdrant Free).
-   **FR-007**: System MUST display exactly one blue floating bubble (bottom-right), and no other floating elements.
-   **FR-008**: System MUST work on mobile devices and instantly follow Docusaurus dark mode settings.
-   **FR-009**: System MUST ensure the widget loads and opens even when offline (showing "no connection" message).
-   **FR-010**: System MUST enable full deployment from scratch in 60 minutes or less.
-   **FR-011**: System MUST ensure that if the chatbot is removed, the book remains 100% perfect and functional.

### Edge Cases

-   What happens when an answer is found in both general text and selected/highlighted text?
-   How does system handle attempts to inject third-party scripts or elements?
-   How does the system gracefully handle a lost internet connection while the widget is active?

## Dependencies and Assumptions

-   The project will be deployed on cloud platforms offering free tiers (e.g., Vercel, Qdrant Cloud Free Tier).
-   "Book's own text" refers to the content hosted within the Docusaurus site.
-   "Selected/highlighted text" refers to explicit user selection or highlighting within the UI.
-   The "gemini key" refers to any API key used for generative AI models, which should be protected from client-side exposure.
-   "Mobile" refers to standard smartphone and tablet screen sizes and touch interactions.
-   "Docusaurus dark mode" refers to the native dark mode feature provided by the Docusaurus framework.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 100% of responses to in-book queries are directly attributable to the book's text.
-   **SC-002**: 100% of responses to out-of-book queries result in an "I don't know" statement.
-   **SC-003**: No third-party scripts or services are present in the deployed application.
-   **SC-004**: The gemini key is never exposed on the client-side (browser).
-   **SC-005**: The application remains operational indefinitely on free-tier cloud services.
-   **SC-006**: Only one blue floating bubble is displayed in the bottom-right, and no other floating UI elements are present.
-   **SC-007**: The application's UI and functionality are fully responsive and adapt instantly to mobile and Docusaurus dark mode settings.
-   **SC-008**: The widget successfully loads and displays an "no connection" message when offline.
-   **SC-009**: A complete deployment from a clean state can be achieved within 60 minutes.
-   **SC-010**: The core book content and functionality are entirely unaffected by the removal of the chatbot component.