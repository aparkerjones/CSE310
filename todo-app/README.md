# To-Do List App

## Overview

I built this browser-based to-do list because it felt like a practical project that I could actually see myself using. I wanted something small enough to finish in a sprint, but still big enough to include interaction, state, styling, and a few language features I needed to demonstrate.

The app lets a user add, edit, delete, and complete tasks. It also saves data with localStorage, so the list stays there after a refresh.

### Purpose

This project gave me a chance to practice a few JavaScript skills:
- **ES6 Array Methods**: Using `.map()`, `.filter()`, `.reduce()`, and `.find()` in the task logic
- **Recursion**: Writing recursive functions for counting active tasks and finding tasks by id
- **Input Validation**: Preventing empty tasks and overly long entries
- **DOM Interaction**: Updating the page based on user actions like clicking, typing, and editing
- **Third-Party Libraries**: Using Alpine.js for lightweight reactivity in the browser

## Development Environment

### Tools Used

- **VS Code** - Used to write and organize the project files
- **Browser DevTools** - Used to test and debug behavior in the browser
- **Git** - Used to track changes while building the project

### Programming Language & Libraries

- **JavaScript (ES6+)** - Core application logic
- **Alpine.js v3** (CDN) - Used for data binding and simple reactive behavior
- **HTML5** - Semantic markup structure
- **CSS3** - Styling, layout, and simple transitions

### Key Dependencies

```html
<script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
```

Alpine.js is loaded through a CDN, so the project runs directly in the browser without a build step.

## Features

### Core Functionality

1. **Add Tasks** - Prevents empty or overly long entries
2. **Edit Tasks** - Modal-based task editing with keyboard shortcuts (Enter to save, Escape to cancel)
3. **Delete Tasks** - Removes individual tasks from the list
4. **Mark Complete** - Toggle task completion status with visual feedback
5. **Filter Tasks** - View to-do, all, or completed tasks using ES6 `.filter()`
6. **Task Statistics** - Real-time display of total, completed, and remaining tasks
7. **Clear Completed** - Bulk delete all completed tasks at once
8. **Persistent Storage** - Saves tasks in browser localStorage
9. **Responsive Design** - Adjusts layout for smaller screens

### JavaScript Concepts Demonstrated

#### ES6 Array Methods

```javascript
// .filter() - Get active tasks
this.tasks = this.tasks.filter(task => !task.completed);

// .map() - Update specific task
this.tasks = this.tasks.map(task => 
    task.id === editId ? { ...task, text: newText } : task
);

// .reduce() - Count completed tasks
this.tasks.reduce((count, task) => count + (task.completed ? 1 : 0), 0);

// .find() - Locate task by ID
this.tasks.find(t => t.id === id);
```

#### Recursion

```javascript
// Recursively calculate total priority of tasks
function calculateTotalPriority(tasks, index = 0) {
    if (index >= tasks.length) return 0;
    const currentPriority = tasks[index].completed ? 0 : 1;
    return currentPriority + calculateTotalPriority(tasks, index + 1);
}

// Recursively find task by ID
function findTaskRecursively(tasks, id, index = 0) {
    if (index >= tasks.length) return null;
    if (tasks[index].id === id) return tasks[index];
    return findTaskRecursively(tasks, id, index + 1);
}
```

#### Input Validation

```javascript
const text = this.newTask.trim();
if (!text) return alert('Task cannot be empty');
if (text.length > 200) return alert('Task cannot exceed 200 characters');
```

## Time Log

### First Week of Sprint

**Monday (2.0 hrs)**
- Created project structure and starter files (`index.html`, `styles.css`, `script.js`)
- Reviewed module requirements and sketched the feature list

**Tuesday (2.5 hrs)**
- Built the initial UI layout (header, input area, task list)
- Added the first working version of adding and displaying tasks

**Wednesday (2.0 hrs)**
- Added complete/delete task behavior
- Wired up filtering for to-do, all, and completed tasks

**Thursday (1.5 hrs)**
- Implemented localStorage save/load logic
- Fixed a couple of small state bugs after reload

**Friday (2.0 hrs)**
- Refactored logic to use ES6 array methods (`map`, `filter`, `reduce`, `find`)
- Added recursion examples required by the module

**Saturday (1.0 hr)**
- CSS cleanup pass and responsive tweaks

### Second Week of Sprint

**Monday (2.0 hrs)**
- Added edit modal and keyboard shortcuts (Enter/Escape)
- Improved interaction flow and task actions

**Tuesday (1.5 hrs)**
- Added input validation for empty and overly long tasks
- Verified user feedback behavior

**Wednesday (2.0 hrs)**
- Added and improved comments for readability
- Reviewed function structure for clarity

**Thursday (2.5 hrs)**
- Debugged Alpine initialization issues
- Fixed HTML attribute/comment parsing bug that broke the input element

**Friday (1.5 hrs)**
- Updated README content to match the final version of the project
- Did a final rubric check and cleaned up a few details before submission

**Saturday (1.0 hr)**
- Final polish pass and checklist review

**Total Time Logged:** 21.5 hours

### User Interface

- **Green Theme** - Forest-green background and button styling
- **Task Cards** - Each task is shown in its own row with edit/delete controls
- **Edit Modal** - Tasks can be updated in a small popup dialog
- **Live Stats** - The page updates task totals automatically
- **Filter Controls** - Lets the user switch between to-do, all, and completed views
- **Responsive Layout** - Works on desktop and smaller screens

## Known Limitations

- This app stores data in browser localStorage, so tasks stay on the same browser/profile only and do not sync across devices.
- There is no backend or account system yet, so clearing browser storage will remove saved tasks.
- Task ordering is basic and there is no drag-and-drop sorting.

## Debugging Notes

- One bug I ran into was caused by putting HTML comments inside an input element's attributes. That broke parsing and made raw attribute text show up on the page.
- I also had to double-check Alpine initialization order so `window.todoApp` was available when the template loaded.
- After fixing those issues, I went back through add, edit, delete, filtering, and localStorage to make sure everything still worked.

## Useful Websites

- [MDN Web Docs - JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - Main reference for JavaScript syntax and features
- [Alpine.js Documentation](https://alpinejs.dev/) - Official Alpine.js guide and examples
- [ES6 Arrow Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions) - Arrow function syntax and usage
- [Array Methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array) - Complete Array methods reference
- [localStorage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) - Browser storage documentation
- [CSS Flexbox Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout) - Helped with layout and spacing
- [HTML Constraint Validation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation) - Practical input validation patterns

## Future Work

- Add task categories or priority labels
- Add due dates
- Add search or sorting options
- Improve accessibility and keyboard navigation
- Connect the app to a backend so tasks could sync across devices

## Building and Running

### Setup

1. Open `index.html` in any modern web browser
2. No build step required - Alpine.js loads via CDN
3. Tasks are automatically saved to browser localStorage

### File Structure

```
todo-app/
├── index.html       # Main HTML with Alpine.js markup
├── styles.css       # Modern CSS with animations
├── script.js        # JavaScript with ES6 features
└── README.md        # This file
```

### Browser Compatibility

- Tested in a current Chrome browser.
- Should work in other modern browsers that support ES6 JavaScript and localStorage.

---

**Author**: Parker Jones
**Date**: March 2026
