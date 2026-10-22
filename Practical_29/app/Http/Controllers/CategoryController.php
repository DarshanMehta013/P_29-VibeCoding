<?php

namespace App\Http\Controllers;

use App\Models\Category;
use Illuminate\Http\Request;

class CategoryController extends Controller
{
    /**
     * Display a listing of book categories.
     */
    public function index()
    {
        $categories = Category::withCount('books')->orderBy('name')->get();
        return view('categories.index', compact('categories'));
    }

    /**
     * Store a newly created category in storage.
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:100|unique:categories,name',
            'code' => 'required|string|max:20|unique:categories,code',
            'description' => 'nullable|string|max:500',
        ]);

        $category = Category::create($validated);

        return redirect()->route('categories.index')
            ->with('success', "Category '{$category->name}' created successfully!");
    }

    /**
     * Update the specified category.
     */
    public function update(Request $request, Category $category)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:100|unique:categories,name,' . $category->id,
            'code' => 'required|string|max:20|unique:categories,code,' . $category->id,
            'description' => 'nullable|string|max:500',
        ]);

        $category->update($validated);

        return redirect()->route('categories.index')
            ->with('success', "Category '{$category->name}' updated successfully!");
    }

    /**
     * Remove the specified category.
     */
    public function destroy(Category $category)
    {
        $bookCount = $category->books()->count();
        if ($bookCount > 0) {
            return back()->with('error', "Cannot delete category '{$category->name}' because it contains {$bookCount} active book titles. Reassign books first.");
        }

        $name = $category->name;
        $category->delete();

        return redirect()->route('categories.index')
            ->with('success', "Category '{$name}' deleted successfully!");
    }
}
