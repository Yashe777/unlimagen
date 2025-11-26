# Mobile UI Guide - Visual Reference

## Mobile Navigation Flow

### Desktop View (≥ 768px)
```
┌─────────────────────────────────────────────────────────┐
│ [Logo]  Home  Resources▼  Pricing  About  Contact      │
│                                        Login │ Sign Up   │
└─────────────────────────────────────────────────────────┘
```

### Mobile View (< 768px)
```
┌──────────────────────────────┐
│ [Logo]                  [☰]  │  ← Hamburger Menu Button
└──────────────────────────────┘

When hamburger is clicked:
┌──────────────────────────────┐
│ [Logo]                  [☰]  │
└──────────────────────────────┘
│█████████████████████████│    │  ← Dark Overlay
│                         │────│
│  ┌──────────────────┐  │    │
│  │ [Logo]        [×]│  │    │  ← Slide-in Menu
│  ├──────────────────┤  │    │
│  │ Home             │  │    │
│  │ Resources     ▼  │  │    │
│  │   - Guide        │  │    │  ← Expandable Dropdown
│  │   - Examples     │  │    │
│  │   - Blog         │  │    │
│  │ Pricing          │  │    │
│  │ About            │  │    │
│  │ Contact          │  │    │
│  │ Login            │  │    │
│  │ Sign Up          │  │    │
│  └──────────────────┘  │    │
│                         │    │
└─────────────────────────┘────┘
```

## Interaction States

### Hamburger Button
```
Default:    Hover/Active:
┌─────┐     ┌─────┐
│  ☰  │ →   │  ☰  │ (lighter color)
└─────┘     └─────┘
```

### Menu Items
```
Default State:
┌────────────────────┐
│ Home               │  (white text on dark)
├────────────────────┤

Hover/Active State:
┌────────────────────┐
│ Home               │  (highlighted text)
├────────────────────┤
```

### Dropdown Toggle
```
Collapsed:              Expanded:
Resources     ▼    →    Resources     ▲
                          - Guide
                          - Examples
                          - Blog
```

## Responsive Layouts

### Home Page Generator (index_modern.html)

**Desktop (≥ 1024px):**
```
┌─────────────────────────────────────────┐
│  Sidebar  │   Main Content   │   Ads   │
│  (Model)  │  (Input/Output)  │ (Right) │
│  (Styles) │                  │         │
└─────────────────────────────────────────┘
```

**Mobile (< 768px):**
```
┌─────────────────┐
│  Input Section  │
├─────────────────┤
│  Model Selector │
├─────────────────┤
│  Style Selector │
├─────────────────┤
│ Output Section  │
└─────────────────┘
```

### Pricing Page

**Desktop:**
```
┌──────────┬──────────┬──────────┐
│   FREE   │  BASIC   │   PRO    │
│          │ ★POPULAR │          │
└──────────┴──────────┴──────────┘
```

**Mobile:**
```
┌──────────┐
│   FREE   │
└──────────┘
┌──────────┐
│  BASIC   │
│ ★POPULAR │
└──────────┘
┌──────────┐
│   PRO    │
└──────────┘
```

### Dashboard

**Desktop:**
```
┌────────────────────────────┐
│  Account Info (2 columns)  │
└────────────────────────────┘
```

**Mobile:**
```
┌──────────────┐
│ Label        │
│ Value        │
├──────────────┤
│ Label        │
│ Value        │
└──────────────┘
```

## Color Scheme

### Navigation Colors
- **Background**: `#1a1a1a` (Dark gray)
- **Text**: `#ffffff` (White)
- **Hover**: `#D4D4DF` (Light gray/purple)
- **Border**: `#2a2a2a` (Slightly lighter dark)

### Mobile Menu
- **Menu Background**: `#1a1a1a`
- **Overlay**: `rgba(0,0,0,0.7)` (70% black)
- **Dropdown Background**: `#0a0a0a` (Very dark)
- **Dropdown Text**: `#a0a0a0` (Medium gray)

### Active/Selected States
- **Selected Item**: `#D4D4DF` color
- **Button Gradient**: `linear-gradient(135deg, #e0e7ff 0%, #f8fafc 100%)`
- **Button Text**: `#1e293b` (Dark blue-gray)

## Animation & Transitions

### Menu Slide-in
```css
/* Closed State */
right: -100%;

/* Open State */
right: 0;

/* Transition */
transition: right 0.3s ease;
```

### Overlay Fade
```css
/* Hidden */
display: none;

/* Visible */
display: block;
opacity: 1;
```

### Dropdown Expand
```css
/* Collapsed */
display: none;

/* Expanded */
display: block;
```

## Touch Targets

All interactive elements follow mobile best practices:
- **Minimum Size**: 48x48 pixels
- **Spacing**: 8-10px between items
- **Padding**: 15px vertical, 10px horizontal

### Examples:
```
Mobile Nav Link:
┌────────────────────────┐
│  padding: 15px 10px    │  ← Touch-friendly
│  Home                  │
└────────────────────────┘

Button:
┌────────────────────┐
│  padding: 14px     │  ← Easy to tap
│  Generate Image    │
└────────────────────┘
```

## Typography Scales

### Desktop
- H1: 48px
- H2: 32px
- Body: 16px
- Navigation: 15px

### Mobile
- H1: 32px
- H2: 24px
- Body: 14px
- Navigation: 16px

## Key CSS Classes Reference

### Structure
- `.top-bar` - Navigation header container
- `.main-nav` - Desktop navigation (hidden on mobile)
- `.mobile-menu-btn` - Hamburger button (visible on mobile)
- `.mobile-menu` - Slide-in menu container
- `.mobile-menu-overlay` - Dark background overlay

### Interactive
- `.mobile-nav-link` - Menu item links
- `.mobile-dropdown-header` - Clickable dropdown trigger
- `.mobile-dropdown-content` - Expandable dropdown items
- `.mobile-menu-close` - Close button (×)

### States
- `.active` - Applied when menu is open
- `:hover` - Highlight state for links
- `.nav-link.active` - Current page indicator

## JavaScript Event Handlers

```javascript
// Open menu
mobileMenuBtn.click() → menu.classList.add('active')

// Close menu
mobileMenuClose.click() → menu.classList.remove('active')
overlay.click() → menu.classList.remove('active')

// Toggle dropdown
dropdownToggle.click() → dropdown.classList.toggle('active')

// Prevent scroll
document.body.style.overflow = 'hidden' | ''
```

## Testing Checklist

✅ **Navigation Tests:**
- [ ] Hamburger button appears on mobile
- [ ] Menu slides in smoothly
- [ ] Overlay appears behind menu
- [ ] Body scroll is prevented when menu open
- [ ] Close button works
- [ ] Tap overlay closes menu
- [ ] Dropdown expands/collapses
- [ ] All links navigate correctly

✅ **Responsive Tests:**
- [ ] 375px width (iPhone SE)
- [ ] 390px width (iPhone 12)
- [ ] 428px width (iPhone Pro Max)
- [ ] 768px width (Tablet breakpoint)
- [ ] 1024px width (Desktop)

✅ **Cross-Browser:**
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari (iOS)
- [ ] Samsung Internet

---
**Visual Guide Version**: 1.0
**Last Updated**: November 26, 2024
