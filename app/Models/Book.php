<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Book extends Model
{
    use HasFactory;

    protected $fillable = [
        'isbn',
        'title',
        'author',
        'category_id',
        'publisher',
        'publication_year',
        'total_copies',
        'available_copies',
        'rack_location',
        'description',
    ];

    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    public function borrowRecords()
    {
        return $this->hasMany(BorrowRecord::class);
    }

    public function activeLoans()
    {
        return $this->hasMany(BorrowRecord::class)->whereIn('status', ['issued', 'overdue']);
    }
}
