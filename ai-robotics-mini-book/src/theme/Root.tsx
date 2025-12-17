/*import React from 'react';
import type {PropsWithChildren} from '@docusaurus/theme-common';

export default function Root({children}: PropsWithChildren): JSX.Element {
  return (
    <>
      {children}
    </>
  );
}*/

/*import React, { PropsWithChildren } from 'react';

export default function Root({ children }: PropsWithChildren<{}>): any {
  return <>{children}</>;
}*/
import React from 'react';
import Chatbot from './components/Chatbot';
import BookChatbot from './components/book'; // Adjust path as necessary

export default function Root({ children, ...props }) {
  // The selectedText is managed by the parent (Root component) which listens for selection events.
  // We need to get the selected text from the window when the chatbot is active.
  const [selectedText, setSelectedText] = React.useState('');

  React.useEffect(() => {
    console.log('Root component mounted - Chatbot should be visible');
  }, []);

  const handleTextSelection = React.useCallback(() => {
    const selection = window.getSelection();
    if (selection && selection.toString().trim().length > 0) {
      setSelectedText(selection.toString());
    } else {
      setSelectedText('');
    }
  }, []);

  // Add event listener on mount to capture text selections
  React.useEffect(() => {
    document.addEventListener('mouseup', handleTextSelection);
    // Clean up listener on unmount
    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
    };
  }, [handleTextSelection]);

  return (
    <>
      {children}
      {/* Chatbot UI - now handles its own positioning */}
      <Chatbot selectedText={selectedText}/>
      {/*<BookChatbot/>*/}
    </>
  );
};